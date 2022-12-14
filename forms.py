"""Forms for notes app."""

from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for creating a new user."""

    username = StringField("Username",
        validators = [InputRequired(), Length(max=20)])
    password = PasswordField("Password",
        validators = [InputRequired(), Length(max=100)])
    email = StringField("Email",
        validators = [InputRequired(), Length(max=50), Email()])
    first_name = StringField("First Name",
        validators = [InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",
        validators = [InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """ Form for logging in user """

    username = StringField("Username",
        validators = [InputRequired(), Length(max=20)])
    password = PasswordField("Password",
        validators = [InputRequired(), Length(max=100)])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

class NoteForm(FlaskForm):
    """Form to create or edit a note"""

    title = StringField("Title",
        validators = [InputRequired(), Length(max=100)])
    content = StringField("Content",
        validators = [InputRequired()])

# class EditNoteForm(FlaskForm):
#     """Form to update a note"""

#     title = StringField("Title",
#         validators = [InputRequired(), Length(max=100)])
#     content = StringField("Content",
#         validators = [InputRequired()])