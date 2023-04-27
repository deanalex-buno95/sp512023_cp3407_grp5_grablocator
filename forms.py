"""
All forms needed for our website – GrabLocator

forms.py
"""


from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, validators


class RegisterForm(FlaskForm):
    driver_id = StringField('ID', validators=[validators.InputRequired(), validators.Length(min=9, max=9)])
    driver_name = StringField('Name', validators=[validators.InputRequired()])
    driver_dob = DateField('Date Of Birth', validators=[validators.InputRequired()])
    driver_hire_date = DateField('Hire Date', validators=[validators.InputRequired()])
    driver_plate_number = StringField('Plate Number', validators=[validators.InputRequired()])
    driver_email = EmailField('Email', validators=[validators.InputRequired()])
    driver_new_password = PasswordField('New Password', validators=[validators.InputRequired(), validators.Length(min=8)])
    driver_confirm_password = PasswordField('Confirm Password', validators=[validators.EqualTo('driver_new_password')])
