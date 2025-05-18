# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('sports', 'Sports'), ('volunteer', 'Volunteer'), ('festival', 'Festival')])
    location = StringField('Location', validators=[DataRequired()])
    lat = FloatField('Latitude')
    lng = FloatField('Longitude')
    start_time = DateTimeField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    photos = FileField('Upload Photo(s)', render_kw={'multiple': True})
    submit = SubmitField('Create Event')

class RSVPForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    num_guests = IntegerField('Number of Guests', validators=[DataRequired()])
    submit = SubmitField('Register Interest')
