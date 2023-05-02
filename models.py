"""Models for Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
b = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """"create User instance"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register_user(cls, username, password, email, first_name, last_name):
        """static class method to create a user with hashed password"""

        hashed = b.generate_password_hash(password).decode("utf8")
        return cls(username=username,
                   password=hashed,
                   email=email,
                   first_name=first_name,
                   last_name=last_name )

    @classmethod
    def authenticate(cls, username, password):
        """static class authenticate a user via username and password"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and b.check_password_hash(user.password, password):
            return user

        else:
            return False



class Note(db.Model):
    """create Note instance"""

    __tablename__ = "notes"


    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.String(100),
        nullable=False
    )

    owner_username = db.Column(
        db.Text(20),
        nullable=False,
        db.ForeignKey('users.username')
    )

    user = db.relationship("User", backref="notes")