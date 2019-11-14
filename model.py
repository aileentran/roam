#Setting up tables in database!


from flask_sqlalchemy import SQLAlchemy 

# allows us to hash/encrypt passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


###############################################################################################
# Creating tables! 

# User table
class User(db.Model):
    """User of Roam with basic user information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75), nullable=False)
    password_hash = db.Column(db.String(128))
    # String based on Twilio's messaging API - '+1234567890'
    phone = db.Column(db.String(15))

    routes = db.relationship("Route", backref="user")


    def __repr__(self):
        """Show user information when return object!"""

        return f"<User user_id={self.user_id} email={self.email} phone={self.phone}>"

    #setting functions to encrypt/hash passwords; RETURNS NONE!
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Routes table
class Route(db.Model):
    """Table of saved routes"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #name of route that user made. set default value to route id
    name = db.Column(db.String(100), nullable=False)

    #starting location
    #start address - will eventually enforce with searchBox 
    start_address = db.Column(db.String(150), nullable=False)
    #name that user inputs to look for location - laymen term's like "Powell Bart"
    #start_name = db.Column(db.String(100))
    #starting seg's latitude - will have to grab from Google Maps API
    start_lat = db.Column(db.Integer)
    #starting seg's longitude - will have to grab from Google Maps API
    start_lng = db.Column(db.Integer)

    #end location
    #end address - will eventually enforce with searchBox
    end_address = db.Column(db.String(150), nullable=False)
    #laymen's name to look up for a specific location 
    #end_name = db.Column(db.String(100))
    #end's latitude - pull from Google Maps API
    end_lat = db.Column(db.Integer)
    #end's longitude - pull from Google Maps API
    end_lng = db.Column(db.Integer)

    # user_id of person who made this route
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    

    #building relationship btwn routes and users tables! 
    # user = db.relationship("User",
    #                      backref="routes")

    def __repr__(self):
        """Readable information about route objects."""

        return f"<Route route id={self.route_id} user id={self.user_id} route name={self.name} start address={self.start_address} starting longitude={self.start_lng} starting latitude={self.start_lat} end address={self.end_address} end longitude={self.end_lng} end latitude={self.end_lat}>"


class Segment(db.Model):
    """Table of segments associated to user's saved routes."""

    __tablename__ = "segments"

    seg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # insures that segments are in the right order in the route
    order_num = db.Column(db.Integer, nullable=False, default=1)

    #starting location
    #start address - will eventually enforce with searchBox 
    start_address = db.Column(db.String(150), nullable=False)
    #name that user inputs to look for location - laymen term's like "Powell Bart"
    start_name = db.Column(db.String(100))
    #starting seg's latitude - will have to grab from Google Maps API
    start_lat = db.Column(db.Integer)
    #starting seg's longitude - will have to grab from Google Maps API
    start_lng = db.Column(db.Integer)

    #end location
    #end address - will eventually enforce with searchBox
    end_address = db.Column(db.String(150), nullable=False)
    #laymen's name to look up for a specific location 
    end_name = db.Column(db.String(100))
    #end's latitude - pull from Google Maps API
    end_lat = db.Column(db.Integer)
    #end's longitude - pull from Google Maps API
    end_lng = db.Column(db.Integer)
    

    # route id that contains this segment
    route_id = db.Column(db.Integer,
                         db.ForeignKey("routes.route_id"))
    #id of associated mode of transportation
    mode_code = db.Column(db.String(5),
                        db.ForeignKey("modes.mode_code"))

    #building relationship btwn segments and routes tables! 
    route = db.relationship("Route",
                            backref=db.backref("segments", order_by=order_num))
    #building relationship between modes table and segments table
    mode = db.relationship("Mode",
                           backref=db.backref("segments", order_by=order_num))

    def __repr__(self):
        """Readable view of segment objects"""

        return f"<Segment seg id={self.seg_id} route id={self.route_id} mode id={self.mode_code} start seg's name={self.start_seg_name} starting longitude={self.start_seg_lng} starting latitude={self.start_seg_lat} end seg's name={self.end_seg_name} end longitude={self.end_seg_lng} end latitude={self.end_seg_lat}>"
        

#Modes of transportation table!
class Mode(db.Model):
    """Different modes of transportation"""

    __tablename__ = "modes"

    mode_code = db.Column(db.String(5), primary_key=True)
    # TODO: name of mode of transportation - should match Google Maps API mode of transportation names!!!
    mode = db.Column(db.String(25), nullable=False)
 
    def __repr__(self):
        """Readable information about the mode of transportation"""

        return f"<Mode mode code={self.mode_code} mode of transportation={self.mode}>"


#################################################################################################
# Creating environment to make tables
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Connecting to ROAM DATABASE!
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///roam"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app

    connect_to_db(app)
    print("Connected to DB.")