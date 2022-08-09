from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm

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

connect_db(app)
db.create_all()

@app.get("/")
def root():
    """Redirects to registration form page."""

    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def registration_form():
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

        flash(f"New user {new_user.name} added!")
        return redirect("/secret")

    else:
        return render_template("registration_form.html", form = form)


@app.rout("/login", methods = ["GET", "POST"])
def login_form():
    """ Show login form to login user and handle user """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["user_id"] = user.username  # keep logged in
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]

    else:
        return render_template("login_form.html", form = form)

@app.get("/secret")
def secret():
    """ Return the text "You made it!" If they get here """

    return "You made it!"