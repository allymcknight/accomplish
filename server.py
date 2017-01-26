from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Comment, Accomplishment
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

@app.route('/login_submit', methods=['POST'])
def login_submit():
    """Check username and password are correct and add to session."""

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
    #send to personal accomplishments
    return redirect('/accomplishments/%s'% str(user.user_id))

@app.route('/register_submit', methods=['POST'])
def register_submit():
    """Add a user to the db and bring to personal accomplishments redirect"""

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('This user already exists. Please log in.')
        return redirect('/login')

    user = User(email=email, password=password, name=name)
    
    db.session.add(user)
    db.session.commit()
    print user.email

    session['user_id'] = user.user_id

    flash("Welcome, %s" % user.name)
    return redirect('/accomplishments/%s'% str(user.user_id))

@app.route('/accomplishments/<int:user_id>')
def show_accomplishments(user_id):
    """Show user accomplishments"""

    if 'user_id' not in session:
        return render_template('/login')
        
    if user_id != session['user_id']:
        return render_template('/login')

    user = User.query.get(user_id)

    return render_template('accomplishments.html', user=user)



if __name__ == "__main__":

    app.debug = True

    connect_to_db(app, 'postgresql:///accomplish')

    DebugToolbarExtension(app)

    app.run()
