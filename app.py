from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm

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
    """Show registration form to create a user."""

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

# @app.post("/register")




# @app.get("/login")



# @app.post("/login")


# @app.get("/secret")