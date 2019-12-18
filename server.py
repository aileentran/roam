from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Route, Segment, Mode 

import googlemaps

import os

from datetime import datetime, timedelta, timezone

# TODO: change IP address to server's ip address!
gmaps = googlemaps.Client(key='AIzaSyB8cOt4MhRxcvoSKJC7M0XaXCvYFPyhCMQ')


app = Flask(__name__)
# required to have secret key to use Flask sessions and debug toolbar 
# generate random 32 bit secret key!  
app.secret_key= os.urandom(32)

# Throws up error if have undefined error in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage: map, search bar, and register/login buttons."""

    return render_template('homepage.html', route=None)

# @app.route('/registration_page')
# def registration_page():
# 	"""Presents registration page to get new user information."""

# 	return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
	"""Saves user information in fb and redirects to login page"""

	email = request.form.get('email')
	password = request.form.get('password')
	reenter = request.form.get('reenter')
	phone = request.form.get('phone')

	user = User.query.filter_by(email = email).first()
	
	# if email already exists in db, redirect to home page  
	if user != None: 
	# and (user.email == email or user.check_password(password) == True):
		# flash('An account is already associated with this email. Please try to register with a different email or login.')
		return 'EMAIL USED'

	# if the user is already in the database based on email and password
	elif user != None and user.email == email and user.check_password(password) == True:

		# flash('You are already in our system. Please login instead.')
		return 'IN SYSTEM'

	# if the password and re-entered password does not match
	elif password != reenter:
		# flash('The passwords did not match. Please try again. ')
		return 'MISMATCH PASSWORD'

	# if a new user and everything is entered correclty 
	else:
		# adding new user to database
		new_user = User(email = email, phone = phone)

		#setting password
		new_user.set_password(password)

		db.session.add(new_user)
		db.session.commit()

		# saving user to session
		user = User.query.filter_by(email = email).first()
		session['user_id'] = new_user.user_id

		return 'Successfully registered'

# @app.route('/login_page')
# def login_page():
# 	"""Show login page"""

# 	return render_template('login.html')

@app.route('/verify', methods = ['POST'])
def login():
	"""Check and verify login information"""

	email = request.form.get('email')
	password = request.form.get('password')

	user = User.query.filter_by(email = email).first()

	#trying to verify user email and password
	if user != None and user.check_password(password) == True:
		# adding user to session 
		session['user_id'] = user.user_id
		#TODO: decide where to redirect it to: dashboard or.. 
		#another version of home page but with access to dashboard
		return 'SUCCESS'
	elif user != None:
		# user exists but wrong password/email
		
		return 'ERROR'
	else:
	
		return 'NOT REGISTERED'

@app.route('/map')
def map_page():
	"""After user has logged in, show map page map: start, stop(s), mode(s), map, and sidebar with access to logout, user info and routes"""

	user_obj = User.query\
               .options(db.joinedload('routes')
               	          .joinedload('segments')
               	          .joinedload('mode'))\
               .get(session['user_id'])

	# LIST OF ROUTES!! 
	# a user can have many routes 
	route_list = user_obj.routes

	return render_template('map.html', user=user_obj, routes=route_list, route=None, seg_info=None)

@app.route('/save_route', methods=["POST"])
def save_route():
	"""User saves new route, including one stop."""

	name = request.form.get('name')
	start_address = request.form.get('startAddress')
	stop_address = request.form.get('stopAddress')
	mode = request.form.get('mode')
	stop_order = request.form.get('stopOrder')
	user_id = User.query.get(session['user_id']).user_id

	# converting JSON to python dictionary
	stop_address = eval(stop_address)
	mode = eval(mode)
	stop_order = eval(stop_order)

	# grabbing end/final stop = last stop 
	# stop_address keys are strings!
	max_stop = 0
	end_address = stop_address['0']
	for stop in stop_address.keys():
		stop = int(stop)
		if stop > max_stop:
			stop = str(stop)
			end_address = stop_address[stop]
	
	# USE GOOGLE MAPS PLACES API TO GET LAT AND LNG
	############## START ################
	start_info = gmaps.places(start_address)
	# list of results, but coordinates is a dictionary of first element at idx 0
	start_coord = start_info['results'][0]['geometry']['location']
	start_lat = start_coord['lat']
	start_lng = start_coord['lng']

	########## FINAL/END DESTINATION ##############
	end_info = gmaps.places(end_address)
	# list of results, but coordinates is a dictionary of first element at idx 0
	end_coord = end_info['results'][0]['geometry']['location']
	end_lat = end_coord['lat']
	end_lng = end_coord['lng']

	########## ALL STOPS (no start address) #############
	# get all stops INCLUDING final/endstop! 
	# save the lat and lng of each stop with.. a dictionary?
	stop_coord = {}
	for stop in stop_address.keys():
		curr_address = stop_address[stop]
		curr_info = gmaps.places(curr_address)
		curr_coord = curr_info['results'][0]['geometry']['location']
		# curr_lat = curr_coord['lat']
		# curr_lng = curr_coord['lng']

		# save into dictionary
		stop_coord[stop] = curr_coord

	# store route info in routes table
	new_route = Route(name=name, start_address=start_address, start_lat=start_lat, start_lng=start_lng, end_address=end_address, end_lat=end_lat, end_lng=end_lng, user_id=user_id)
	db.session.add(new_route)
	db.session.commit()

	# go through stop info and save to segments table
	# need to extract lat and lng for each stop from stop_coord dictionary
	# using stop key to access all other dictionaries: stop_address, stop_coord, mode, stop_order
	for stop in stop_address.keys():

		stop = int(stop)
		seg_start = ""
		seg_start_lat = ""
		seg_start_lng = ""

		seg_stop = ""
		seg_stop_lat = ""
		seg_stop_lng = ""

		# must be an integer! 
		mode_id = 0
		order_num = 0
		route_id = 0

		# for the first segment, start of segment is actual start address
		if stop == 0:
			seg_start = start_address
			seg_start_lat = start_lat
			seg_start_lng = start_lng

		else:
			seg_start = stop_address[str(stop - 1)]
			seg_start_lat = stop_coord[str(stop - 1)]['lat']
			seg_start_lng = stop_coord[str(stop - 1)]['lng']

		# grabbing stop addresses
		seg_stop = stop_address[str(stop)]
		seg_stop_lat = stop_coord[str(stop)]['lat']
		seg_stop_lng = stop_coord[str(stop)]['lng']

		# adding mode of this segment to modes table
		# go through dictionary and save individual modes to table	
		md = Mode(mode=mode[str(stop)])
		db.session.add(md)
		db.session.commit()

		mode_id = md.mode_id
		order_num = stop_order[str(stop)]
		route_id = new_route.route_id

		# adding each segment into segments table!

		segment = Segment(order_num=order_num, start_address=seg_start, start_lat=seg_start_lat, start_lng=seg_start_lng, stop_address=seg_stop, stop_lat=seg_stop_lat, stop_lng=seg_stop_lng, route_id=route_id, mode_id=mode_id)
		db.session.add(segment)
		db.session.commit()

	return 'SUCCESS'

@app.route('/map/<int:route_id>')
def route_info(route_id):
	"""Shows route information AS JSON!"""

	route_obj = Route.query\
					.options(db.joinedload('segments')
								.joinedload('mode'))\
					.get(route_id)

	# information about each segment
	seg_info={
		"routeName": route_obj.name.title(),
	} 


	# total_seconds = 0

	for idx, segment in enumerate(route_obj.segments):
		route_info = gmaps.distance_matrix(segment.start_address, segment.stop_address, segment.mode.mode, departure_time=datetime.now())
		print(route_info)

		# return example: 
		# {'destination_addresses': ['1825 4th St, San Francisco, CA 94158, USA'], 'origin_addresses': ['1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA'], 'rows': [{'elements': [{'distance': {'text': '54.8 km', 'value': 54814}, 'duration': {'text': '38 mins', 'value': 2307}, 'status': 'OK'}]}], 'status': 'OK'}
		# NOTE: duration value = time expressed in seconds 

		# getting idx to match order num of segment
		start = route_info['origin_addresses'][0]
		stop = route_info['destination_addresses'][0]
		distance_km = route_info['rows'][0]['elements'][0]['distance']['text']
		duration_text = route_info['rows'][0]['elements'][0]['duration']['text']
		# duration_int = int(duration_text.split(' ')[0])
		seconds = route_info['rows'][0]['elements'][0]['duration']['value']




		# total_seconds += seconds

		# TODO: CONVERT TIME INTO CURRENT TIMEZONE!!!!!
		# calculate ETA - hardcoded to PST 
		# convert from utc to local time 


		# print('this is now')
		# print(datetime.now())

		# print('seconds')
		# print(seconds)

		# print('minutes')
		# print(seconds / 60)

		# print(datetime.now() + timedelta(seconds=seconds))

		# PST = datetime.now() - timedelta(hours = 8)
		# print('this is now in PST')
		# print(PST)

		# eta = PST + timedelta(seconds=seconds)
		# print('eta!')
		# print(eta)

		# eta_str = eta.strftime('%a %b %d, %Y at %I:%M %p')
		# print('prettier eta')
		# print(eta_str)

		# print('\n\n\n\n')


		# live traffic times ONLY FOR DRIVING 
		# duration_in_traffic 
		# {'destination_addresses': ['1428 5th St, Oakland, CA 94607, USA'], 'origin_addresses': ['647 El Cerro Dr, El Sobrante, CA 94803, USA'], 'rows': [{'elements': [{'distance': {'text': '24.4 km', 'value': 24411}, 'duration': {'text': '20 mins', 'value': 1211}, 'duration_in_traffic': {'text': '25 mins', 'value': 1486}, 'status': 'OK'}]}], 'status': 'OK'}
		if segment.mode.mode == 'driving':

			duration_in_traffic_text = route_info['rows'][0]['elements'][0]['duration_in_traffic']['text']
			duration_in_traffic_seconds = route_info['rows'][0]['elements'][0]['duration_in_traffic']['value']

			print(duration_in_traffic_text)
			print(duration_in_traffic_seconds)
			print('\n\n\n\n')

			seg_info[f'segment_{idx + 1}']={
				'start': start,
				'stop': stop, 
				'mode': segment.mode.mode.title(),
				'distance': distance_km,
				'duration': duration_in_traffic_text,
				# 'durationInt': duration_int,
				'seconds': duration_in_traffic_seconds,
				# 'eta': eta_str,
				'order': segment.order_num
			}

		# include fare cost if segment mode is transit
		elif segment.mode.mode == 'transit':
			seg_info[f'segment_{idx + 1}']={
			'start': start,
			'stop': stop, 
			'mode': segment.mode.mode.title(),
			'distance': distance_km,
			'duration': duration_text,
			# 'durationInt': duration_int,
			'seconds': seconds,
			# 'eta': eta_str,
			'currency': route_info['rows'][0]['elements'][0]['fare']['currency'],
			'fare': route_info['rows'][0]['elements'][0]['fare']['text'],
			'order': segment.order_num
		}

		else:
			seg_info[f'segment_{idx + 1}']={
				'start': start,
				'stop': stop, 
				'mode': segment.mode.mode.title(),
				'distance': distance_km,
				'duration': duration_text,
				# 'durationInt': duration_int,
				'seconds': seconds,
				# 'eta': eta_str,
				'order': segment.order_num
			}

	return jsonify(seg_info)

@app.route('/map/<int:route_id>/directions')
def directions(route_id):
	"""JSON information about route."""

	route_obj = Route.query\
					.options(db.joinedload('segments')
								.joinedload('mode'))\
					.get(route_id)

	seg_info = [
		{
			"id": segment.seg_id,
			"orderNum": segment.order_num,
			"start_lat": segment.start_lat,
			"start_lng": segment.start_lng,
			"stop_lat": segment.stop_lat,
			"stop_lng": segment.stop_lng,
			"mode": segment.mode.mode
		}

		for segment in route_obj.segments
	]

	return jsonify(seg_info)

@app.route('/log-out')
def log_out():
	"""Logs out user"""

	session.pop('user_id')
	# flash('You are logged out. See you next time!')

	return redirect('/')


if __name__ == "__main__":
    app.debug = False
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    print("Connected to DB.")

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=False)