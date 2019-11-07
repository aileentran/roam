from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Route, Segment, Mode 


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

##################################################################
# Guest user experience! 







##################################################################
# Registered user experience###########################

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
		session["user"] = user.email
		flash('You are logged in. Welcome!')
		#TODO: decide where to redirect it to: dashboard or.. 
		#another version of home page but with access to dashboard
		return redirect('/')
	elif user != None:
		flash('Your email or password is incorrect. Please try again.')
		
		return redirect('/login_page')
	else:
		flash('You are not a registered user. If you want to register, please click the Register button to continue.')
		return redirect('/')



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    print("Connected to DB.")

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)