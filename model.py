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
    start_address = db.Column(db.String(150), nullable=False)
    #starting seg's latitude - will have to grab from Google Maps API
    start_lat = db.Column(db.Float)
    #starting seg's longitude - will have to grab from Google Maps API
    start_lng = db.Column(db.Float)

    #end location
    end_address = db.Column(db.String(150), nullable=False)
    #end's latitude - pull from Google Maps API
    end_lat = db.Column(db.Float)
    #end's longitude - pull from Google Maps API
    end_lng = db.Column(db.Float)

    # user_id of person who made this route
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))

    def __repr__(self):
        """Readable information about route objects."""

        return f"<Route route id={self.route_id} user id={self.user_id} route name={self.name} start address={self.start_address} starting latitude={self.start_lat} starting longitude={self.start_lng} end address={self.end_address} end latitude={self.end_lat} end longitude={self.end_lng}>"


class Segment(db.Model):
    """Table of segments associated to user's saved routes."""

    __tablename__ = "segments"

    seg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # insures that segments are in the right order in the route
    order_num = db.Column(db.Integer, nullable=False, default=1)

    #starting location
    start_address = db.Column(db.String(150), nullable=False)
    #starting seg's latitude - will have to grab from Google Maps API
    start_lat = db.Column(db.Float)
    #starting seg's longitude - will have to grab from Google Maps API
    start_lng = db.Column(db.Float)

    #end location
    stop_address = db.Column(db.String(150), nullable=False)
    #end's latitude - pull from Google Maps API
    stop_lat = db.Column(db.Float)
    #end's longitude - pull from Google Maps API
    stop_lng = db.Column(db.Float)
    

    # route id that contains this segment
    route_id = db.Column(db.Integer,
                         db.ForeignKey("routes.route_id"))
    #id of associated mode of transportation
    mode_id = db.Column(db.Integer,
                        db.ForeignKey("modes.mode_id"))

    #building relationship btwn segments and routes tables! 
    route = db.relationship("Route",
                            backref=db.backref("segments", order_by=order_num))
    #building relationship between modes table and segments table
    mode = db.relationship("Mode",
                           backref=db.backref("segments", order_by=order_num))

    def __repr__(self):
        """Readable view of segment objects"""

        return f"<Segment seg id={self.seg_id} route id={self.route_id} mode id={self.mode_id} start seg's address={self.start_address} starting latitude={self.start_lat} starting longitude={self.start_lng} stop seg's address={self.stop_address} stop latitude={self.stop_lat} end longitude={self.stop_lng}>"
        

#Modes of transportation table!
class Mode(db.Model):
    """Different modes of transportation"""

    __tablename__ = "modes"

    mode_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # TODO: name of mode of transportation - should match Google Maps API mode of transportation names!!!
    mode = db.Column(db.String(25), nullable=False)
 
    def __repr__(self):
        """Readable information about the mode of transportation"""

        return f"<Mode id ={self.mode_id} mode of transportation={self.mode}>"

# Creating environment to make tables
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Connecting to ROAM DATABASE!
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///roam"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("Connected to DB.")