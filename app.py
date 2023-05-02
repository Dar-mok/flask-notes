"""Flask app for CupcNotesakes"""

import os

from flask import Flask, render_template, flash, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get("/")
def redirect_register():
    """redirect to /register"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """If completed register form, create User object and save
     to DB and redirect to user's page, else, render the register form"""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register_user(name, pwd, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username
        return redirect(f"users/{name}")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """either show a login form or login user"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.login_user(name, pwd)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{name}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("register.html", form=form)

