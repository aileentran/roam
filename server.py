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
    """Homepage: map, search bar, and register/login buttons"""

    return render_template('homepage.html')



if __name__ == "__main__":
    connect_to_db(app)
    print("Connected to DB.")

    app.run(host="0.0.0.0", debug=True)