from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

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
		return redirect('/logged_in')
	elif user != None:
		flash('Your email or password is incorrect. Please try again.')
		
		return redirect('/login_page')
	else:
		flash('You are not a registered user. If you want to register, please click the Register button to continue.')
		return redirect('/')

@app.route('/logged_in')
def logged_in_page():
	"""Shows logged in page: start, stop(s), mode(s), map, and sidebar with access to logout, user info and routes"""

	return render_template('logged_in.html')

@app.route('/save_route', methods=['POST'])
def save_route():
	"""User saves new route."""

	# get route name - get from form!
	route_name = request.form.get('name')

	# get start address - from form 
	start_address = request.form.get('start')
	# get end address - from form
	end_address = request.form.get('stop')

	# get user obj - grab the right user then pass in user id
	user_obj = User.query.get(session['user_id'])
	

	# USE GOOGLE MAPS API TO GET INFO! 
	# get start lat - using start address
	# this is a LIST of info!! 
	start_info = gmaps.geocode(start_address)

	#result: 
	# [{'address_components': [{'long_name': '1600', 'short_name': '1600', 'types': ['street_number']}, {'long_name': 'Amphitheatre Parkway', 'short_name': 'Amphitheatre Pkwy', 'types': ['route']}, {'long_name': 'Mountain View', 'short_name': 'Mountain View', 'types': ['locality', 'political']}, {'long_name': 'Santa Clara County', 'short_name': 'Santa Clara County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'California', 'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '94043', 'short_name': '94043', 'types': ['postal_code']}], 'formatted_address': '1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA', 'geometry': {'location': {'lat': 37.4215785, 'lng': -122.0837816}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 37.42292748029149, 'lng': -122.0824326197085}, 'southwest': {'lat': 37.4202295197085, 'lng': -122.0851305802915}}}, 'place_id': 'ChIJtYuu0V25j4ARwu5e4wwRYgE', 'plus_code': {'compound_code': 'CWC8+JF Mountain View, California, United States', 'global_code': '849VCWC8+JF'}, 'types': ['street_address']}]


	for info in start_info:
		if 'geometry' in info:
			print('hi')

	
	# start lng - using start address
	# end lat - using end address
	# end lng - using end address 

	# store in database! 

	# render new page 
	#####frontend##### 
	# with route in dropdown 
	# map with markers
	# path to get there
	# estimated arrival times 

	return redirect('/')



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    print("Connected to DB.")

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)