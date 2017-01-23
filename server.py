from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
import os

app = Flask(__name__)


app.secret_key = os.environ['flask_app_key']
#avoid error message
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return "<html><body>Placeholder for the homepage.</body></html>"

@app.route('/login')
def login_form():
    """Shows register and login form"""

    return render_template('login.html')


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app, 'postgresql:///accomplish')

    DebugToolbarExtension(app)

    app.run()
