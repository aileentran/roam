from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Route, Segment, Mode 

import googlemaps

from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyB8cOt4MhRxcvoSKJC7M0XaXCvYFPyhCMQ')


app = Flask(__name__)
# required to have secret key to use Flask sessions and debug toolbar
# TODO: CHANGE SECRET KEY!! 
app.secret_key='SUPER SECRET'

# Throws up error if have undefined error in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage: map, search bar, and register/login buttons."""

    return render_template('homepage.html')

@app.route('/registration_page')
def registration_page():
	"""Presents registration page to get new user information."""

	return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
	"""Saves user information in fb and redirects to login page"""

	email = request.form.get('email')
	password = request.form.get('password')
	reenter = request.form.get('re-enter')
	phone = request.form.get('phone')

	user = User.query.filter_by(email = email).first()
	
	# if email already exists in db, redirect to home page  
	if user != None: 
	# and (user.email == email or user.check_password(password) == True):
		flash('An account is already associated with this email. Please try to register with a different email or login.')
		return redirect('/')

	# if the user is already in the database based on email and password
	elif user != None and user.email == email and user.check_password(password) == True:

		flash('You are already in our system. Please login instead.')
		return redirect('/login_page')

	# if the password and re-entered password does not match
	elif password != reenter:
		flash('The passwords did not match. Please try again. ')
		return redirect('/registration_page')

	# if a new user and everything is entered correclty 
	else:
		# adding new user to database
		new_user = User(email = email, phone = phone)

		#setting password
		new_user.set_password(password)

		db.session.add(new_user)
		db.session.commit()
		flash('You have successfully registered!')
		return redirect('/login_page')

@app.route('/login_page')
def login_page():
	"""Show login page"""

	return render_template('login.html')

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
		flash('You are logged in. Welcome!')
		#TODO: decide where to redirect it to: dashboard or.. 
		#another version of home page but with access to dashboard
		return redirect('/map')
	elif user != None:
		flash('Your email or password is incorrect. Please try again.')
		
		return redirect('/login_page')
	else:
		flash('You are not a registered user. If you want to register, please click the Register button to continue.')
		return redirect('/')

@app.route('/map')
def map_page():
	"""After user has logged in, show map page map: start, stop(s), mode(s), map, and sidebar with access to logout, user info and routes"""

	return render_template('map.html')

@app.route('/save_route', methods=['POST'])
def save_route():
	"""User saves new route, including one stop."""

	# get route name - get from form!
	route_name = request.form.get('name')
	# get start address - from form 
	start_address = request.form.get('start')

	# get stop info - from form 
	stop_address = request.form.get('stop')
	mode_stop = request.form.get('mode_stop')
	stop_order = request.form.get('seg_order_stop')

	# get end info - from form 
	end_address = request.form.get('end')
	mode_end = request.form.get('mode_end')
	end_order = request.form.get('seg_order_end')

	# get user obj - grab the right user then pass in user id
	user_obj = User.query.get(session['user_id'])
	# user id - will save in routes table
	user_id = user_obj.user_id
	

	# USE GOOGLE MAPS API TO GET INFO! 

	########## START ############
	# get start coordinates - using start address
	# this is a dictionary of places info!! 
	start_info = gmaps.places(start_address)
	# list of results, but coordinates is a dictionary of first element at idx 0
	start_coord = start_info['results'][0]['geometry']['location']
	start_lat = start_coord['lat']
	start_lng = start_coord['lng']

	########## STOP ###############
	# get stop coordinates using address
	# this is a dictionary of places info!! 
	stop_info = gmaps.places(stop_address)
	# list of results, but coordinates is a dictionary of first element at idx 0
	stop_coord = stop_info['results'][0]['geometry']['location']
	stop_lat = stop_coord['lat']
	stop_lng = stop_coord['lng']
	
	############# END #############
	# get end coordinates using address
	# this is a dictionary of places info!! 
	end_info = gmaps.places(end_address)
	# list of results, but coordinates is a dictionary of first element at idx 0
	end_coord = end_info['results'][0]['geometry']['location']
	end_lat = end_coord['lat']
	end_lng = end_coord['lng']

	# store start and end in route table
	new_route = Route(name=route_name, start_address=start_address, start_lat=start_lat, start_lng=start_lng, end_address=end_address, end_lat=end_lat, end_lng=end_lng, user_id=user_id)
	db.session.add(new_route)
	db.session.commit()

	# store first mode in mode table
	first_mode = Mode(mode=mode_stop)
	db.session.add(first_mode)
	db.session.commit()

	# store second mode in mode table 
	second_mode = Mode(mode=mode_end)
	db.session.add(second_mode)
	db.session.commit()

	# store first segment in segment table
	first_seg = Segment(order_num=stop_order, start_address=start_address, start_lat=start_lat, start_lng=start_lng, stop_address=stop_address, stop_lat=stop_lat, stop_lng=stop_lng, route_id=new_route.route_id, mode_id=first_mode.mode_id)
	db.session.add(first_seg)
	db.session.commit()

	# store second segment in segment table
	second_seg = Segment(order_num=end_order, start_address=stop_address, start_lat=stop_lat, start_lng=stop_lng, stop_address=end_address, stop_lat=end_lat, stop_lng=end_lng, route_id=new_route.route_id, mode_id=second_mode.mode_id)
	db.session.add(second_seg)
	db.session.commit()

	flash('Your new route has been successfully added! You can view it by hitting the "Route" tab. :)')

	return redirect('/map')

@app.route('/users-routes')
def users_routes():
	"""Show all the saved routes."""

	# joining routes, segments, and mode tables for specified user
	# reduces the number of queries
	# user_obj has access to all route info!
	user_obj = User.query\
	               .options(db.joinedload('routes')
	               	          .joinedload('segments')
	               	          .joinedload('mode'))\
	               .get(session['user_id'])

	# LIST OF ROUTES!! 
	# a user can have many routes 
	route_list = user_obj.routes


	return render_template('users-routes.html', user=user_obj, routes=route_list)

@app.route('/map/<int:route_id>')
def route_info(route_id):
	"""Shows route information on map page."""

	route_obj = Route.query\
					.options(db.joinedload('segments')
								.joinedload('mode'))\
					.get(route_id)

	# information about each segment 
	for segment in route_obj.segments:
		route_info = gmaps.distance_matrix(segment.start_address, segment.stop_address, segment.mode.mode)
		print(route_info)

	return render_template('map.html')


@app.route('/log-out')
def log_out():
	"""Logs out user"""

	session.pop('user_id')
	flash('You are logged out. See you next time!')

	return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    print("Connected to DB.")

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)