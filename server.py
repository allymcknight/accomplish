from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, session, request, flash
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

@app.route('/login_submit')
def login_submit():

    email = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("We couldn't find your email, sorry. Try again.")
        return redirect('/login')
    if user.password != password:
        flash("That's not the right password for this username. Try again.")
        return redirect('/login')

    session['user_id'] = user.user_id

    flash("Welcome, %s" % user.name)
    return redirect('/accomplishments/%s'% str(user.user_id))





if __name__ == "__main__":

    app.debug = True

    connect_to_db(app, 'postgresql:///accomplish')

    DebugToolbarExtension(app)

    app.run()
