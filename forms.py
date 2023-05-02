"""Forms for playlist app."""

from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
                    "Username",
                    validators=[
                        InputRequired(),
                        Length(min=1, max=20)
                    ]
                )

    password = PasswordField(
                    "Password",
                    validators=[
                        InputRequired(),
                        Length(min=8, max=100)
                    ]
                )

    email = StringField(
                    "Email",
                    validators=[
                        InputRequired(),
                        Email(),
                        Length(min=1, max=50)
                    ]
                )

    first_name = StringField(
                    "First Name",
                    validators=[
                        InputRequired(),
                        Length(min=1, max=30)
                    ]
                )

    last_name = StringField(
                    "Last Name",
                    validators=[
                        InputRequired(),
                        Length(min=1, max=30)
                        ]
                )

class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
                    "Username",
                    validators=[
                        InputRequired(),
                        Length(min=1, max=20)
                    ]
                )

    password = PasswordField(
                    "Password",
                    validators=[
                        InputRequired(),
                        Length(min=8, max=100)
                    ]
                )

class CSRFProtectForm(FlaskForm):
    """Form to validate logout"""