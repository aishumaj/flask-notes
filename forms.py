"""Forms for notes app."""

from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length, Email, email_validator


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
