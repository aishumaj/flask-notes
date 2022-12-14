from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

SESSION_KEY = 'username'

connect_db(app)
db.create_all() #better to do this explicitly in ipython

@app.get("/")
def root():
    """Redirects to registration form page."""

    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def register_user():
    """Show registration form to create a user and handle creating user"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        #create user
        new_user = User.register(username = username, password = password,
            email = email, first_name = first_name, last_name = last_name)

        db.session.add(new_user)
        db.session.commit()

        session[SESSION_KEY] = new_user.username

        flash(f"New user {new_user.username} added!")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("registration_form.html", form = form)


@app.route("/login", methods = ["GET", "POST"])
def login_user():
    """ Show login form to login user and handle user """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session[SESSION_KEY] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]

    # else: need to not have this because this will prevent rendering template even with error
    return render_template("login_form.html", form = form)

@app.get("/users/<username>")
def show_user_details(username):
    """ Show user details If they are logged in and correct user"""

    if SESSION_KEY not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif session[SESSION_KEY] != username:
        flash("Please don't try to access other users' pages, thank you!")
        return redirect(f"/users/{session[SESSION_KEY]}")

    user = User.query.get_or_404(username)
    form = CSRFProtectForm() #no data coming in request, so we're making blank form

    return render_template("user_details.html", user=user, form=form)

@app.post("/logout")
def logout_user():
    """ Logout current user and remove session data and redirect to home page"""

    form = CSRFProtectForm() #has the information of the form submission (the CSRF token)
    # same as putting in request.form inside parentheses... very different from above
    # might be form.data instead of request.form

    if form.validate_on_submit():
        # Remove SESSION_KEY if present, but no errors if it wasn't
        session.pop(SESSION_KEY, None)

    return redirect("/")

# ask about chrome saying password in data breach popup
# just happens a lot on local host, dw

@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user account and all of their notes"""
    if SESSION_KEY not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif session[SESSION_KEY] != username:
        flash("Please don't try to access other users' pages, thank you!")
        return redirect(f"/users/{session[SESSION_KEY]}")

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    if form.validate_on_submit():
        Note.query.filter_by(owner=username).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop(SESSION_KEY, None)

    return redirect("/")

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    """Returns add new note form and handles form data on submission."""

    if SESSION_KEY not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif session[SESSION_KEY] != username:
        flash("Please don't try to access other users' pages, thank you!")
        return redirect(f"/users/{session[SESSION_KEY]}")

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title = title, content = content, owner = username)

        db.session.add(new_note)
        db.session.commit()

        flash("New note added!")
        return redirect(f"/users/{username}")

    else:
        return render_template("add_note.html", form = form)

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_notes(note_id):
    """ Display note update form and handle submission of note updates."""

    note = Note.query.get_or_404(note_id)

    if SESSION_KEY not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif session[SESSION_KEY] != note.owner:
        flash("Please don't try to access other users' pages, thank you!")
        return redirect(f"/users/{session[SESSION_KEY]}")

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash(f"Note {note.title} updated!")
        return redirect(f"/users/{note.owner}")

    else:
        return render_template("edit_note.html", form = form)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """ Delete a specific note."""

    note = Note.query.get_or_404(note_id)

    if SESSION_KEY not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    elif session[SESSION_KEY] != note.owner:
        flash("Please don't try to access other users' pages, thank you!")
        return redirect(f"/users/{session[SESSION_KEY]}")

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted!")
        return redirect(f"/users/{note.owner}")



