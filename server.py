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

    return render_template('homepage.html', route=None)

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

	return render_template('map.html', route=None, seg_info=None)

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

	# grabbing final stop = last stop 
	# stop_address keys are strings!
	max_stop = 0
	final = ''
	for stop in stop_address.keys():
		stop = int(stop)
		if stop > max_stop:
			stop = str(stop)
			final = stop_address[stop]
	print(final)

	# do database stuff with the info
	# return whatever we want

	flash('Your new route has been successfully added! You can view it by hitting the "Route" tab. :)')

	return jsonify({'the year is 3833, sentient yogurt rules the land': 'no'})

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
	seg_info={} 
	for idx, segment in enumerate(route_obj.segments):
		route_info = gmaps.distance_matrix(segment.start_address, segment.stop_address, segment.mode.mode)

		# TODO: figure out if want to pass in details OR entire route info
		# accessing distance, duration, and fare
		details = route_info['rows'][0]['elements'][0]
		# getting idx to match order num of segment
		seg_info[f'Segment {idx + 1}']=details

	return render_template('map.html', route=route_obj, seg_info=seg_info)

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
	flash('You are logged out. See you next time!')

	return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    print("Connected to DB.")

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)