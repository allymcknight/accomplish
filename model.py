"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    is_student = db.Column(db.Boolean, nullable=True)
    is_working = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)


class Accomplishment(db.Model):
    """Accomplishment of user"""

    __tablename__ = "accomplishments"

    accomplishment_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    text = db.Column(db.Text)
    proof = db.Column(db.String(300), nullable=True)
    category_type = db.Column(db.String(40))
    needs_boost = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime)

    user = db.relationship("User", backref=db.backref("accomplishments"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Accomplishment accomplishment_id=%s text=%s>" % (self.accomplishment_id,
                                               self.text)


class Comment(db.Model):
    """Comment on accomplishment"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    accomplishment_id = db.Column(db.Integer, db.ForeignKey('accomplishments.accomplishment_id'))
    comment_text = db.Column(db.Text)
    commenter_id = db.Column(db.Integer)

    accomplishment = db.relationship("Accomplishment", backref=db.backref("comments"))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Comment comment_id=%s text=%s" % (self.comment_id,
                                                   self.comment_text)

#####################################################################
# Helper functions

def connect_to_db(app, db_uri):
    """Connect the database in Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app,'postgresql:///accomplish')
    print "Connected to DB."