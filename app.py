"""Flask app for Notes"""

import os

from flask import Flask, render_template, flash, redirect, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, UpdateNoteForm, AddNoteForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")

USER_ID = "user_id"

connect_db(app)

db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get("/")
def redirect_register():
    """redirect to /register"""

    return redirect("/register")

#--------USER ROUTES--------

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

        session[USER_ID] = user.username
        return redirect(f"users/{name}")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """either show a login form or login user"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        if user:
            session[USER_ID] = user.username
            return redirect(f"/users/{name}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.get("/users/<username>")
def info_user_notes(username):
    """display user profile page with notes info"""

    if not session.get(USER_ID) == username:
        flash("You must be logged in to see that page!")

        return redirect("/login")

    form = CSRFProtectForm()
    user = User.query.get_or_404(username)

    return render_template("profile_page.html", user=user, form=form)

@app.post("/users/<username>/delete")
def delete_user(username):
    """display user profile page with notes info"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)

        session.pop(USER_ID, None)

        db.session.delete(user)
        db.session.commit

    return redirect('/')

@app.post("/logout")
def logout():
    """logout user by clearing session"""

    form = CSRFProtectForm()

    if form.validate_on_submit():

        session.pop(USER_ID, None)

    return redirect("/login")

#--------NOTES ROUTES--------
@app.route("/user/<username>/notes/add", methods=["POST", "GET"])
def add_note(username):
    """display form to add a note"""

    form = AddNoteForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        owner = username

        note = Note(title=title, content=content, owner_username=owner)

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{owner}')

    return render_template('note_add_form.html', form=form)


@app.route("/notes/<int:note_id>/update", methods=["POST", "GET"])
def update_note(note_id):
    """display form to edit a note"""

    note = Note.query.get_or_404(note_id)

    form = UpdateNoteForm()


    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{note.user.username}')

    return render_template('note_edit_form.html', note=note, form=form)



