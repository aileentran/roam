#Setting up tables in database!

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
db = SQLAlchemy()
#################################################################################################
# Creating environment to make tables
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Connecting to ROAM DATABASE!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///roam'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    connect_to_db(app)
    print("Connected to DB.")


###############################################################################################
# Creating tables! 

# User table
class User(db.Model):
	"""User of Roam with basic user information"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(75), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	# String based on Twilio's messaging API - '+1234567890'
	phone = db.Column(db.String(15))


	def __repr__(self):
		"""Show user information when return object!"""

		return f"<User id: {self.user_id} email: {self.email} phone: {self.phone}>"

# Routes table
class Route(db.Model):
	"""Table of saved routes"""

	__tablename__ = "routes"

	route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# user_id of person who made this route
	user_id = db.Column(db.Integer,
						db.ForeignKey("users.user_id"))
	#name of route that user made. set default value to route id
	name = db.Column(db.String(100), nullable=False)

	#starting location
	#name that user inputs to look for location - laymen term's like "Powell Bart"
	start_name = db.Column(db.String(100), nullable=False)
	#starting point's longitude - will have to grab from Google Maps API
	start_lng = db.Column(db.Integer, nullable=False)
	#starting point's latitude - will have to grab from Google Maps API
	start_lat = db.Column(db.Integer, nullable=False)

	#end location
	#laymen's name to look up for a specific location 
	end_name = db.Column(db.String(100), nullable=False)
	#end point's longitude - pull from Google Maps API
	end_lng = db.Column(db.Integer, nullable=False)
	#end point's latitude - pull from Google Maps API
	end_lat = db.Column(db.Integer, nullable = False)

	#building relationship btwn routes and users tables! 
	user = db.relationship("User",
							db.backref("routes"))

	def __repr__(self):
		"""Readable information about route objects."""

		return f"<Route id: {self.route_id} user id: {self.user_id} route name: {self.name} start location's name: {self.start_name} starting longitude: {self.start_lng} starting latitude: {self.start_lat} end location's name: {self.end_name} end longitude: {self.end_lng} end latitude: {self.end_lat}>"

class Segment(db.Model):
	"""Table of segments associated to user's saved routes."""

	__tablename__ = "segments"

	seg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# route id that contains this segment
	route_id = db.Column(db.Integer,
						db.ForeignKey("routes.route_id"))
	#id of associated mode of transportation
	mode_id = db.Column(db.Integer,
						db.ForeignKey("modes.mode_id"))

	#starting location
	#name that user inputs to look for location - laymen term's like "Powell Bart"
	start_seg_name = db.Column(db.String(100), nullable=False)
	#starting seg's longitude - will have to grab from Google Maps API
	start_seg_lng = db.Column(db.Integer, nullable=False)
	#starting seg's latitude - will have to grab from Google Maps API
	start_seg_lat = db.Column(db.Integer, nullable=False)

	#end location
	#laymen's name to look up for a specific location 
	end_seg_name = db.Column(db.String(100), nullable=False)
	#end's longitude - pull from Google Maps API
	end_seg_lng = db.Column(db.Integer, nullable=False)
	#end's latitude - pull from Google Maps API
	end_seg_lat = db.Column(db.Integer, nullable = False)

	#building relationship btwn segments and routes tables! 
	route = db.relationship("Route",
							db.backref("segments"))
	#building relationship between modes table and segments table
	mode = db.relationship("Mode",
							db.backref("segments"))

	def __repr__(self):
		"""Readable view of segment objects"""

		return f"<Seg id: {self.seg_id} route id: {self.route_id} mode id: {self.mode_id} start seg's name: {self.start_seg_name} starting longitude: {self.start_seg_lng} starting latitude: {self.start_seg_lat} end seg's name: {self.end_seg_name} end longitude: {self.end_seg_lng} end latitude: {self.end_seg_lat}>"

#Modes of transportation table!
class Mode(db.Model):
	"""Different modes of transportation"""

	__tablename__ = "modes"

	mode_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	#name of mode of transportation - should match Google Maps API mode of transportation names!!!
	mode = db.Column(db.String(25), nullable=False)

	def __repr__(self):
		"""Readable information about the mode of transportation"""

		return f"<Mode id: {self.mode_id} mode of transportation: {self.mode}>"




