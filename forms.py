"""
All forms needed for our website – GrabLocator

forms.py
"""


from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, EmailField, PasswordField, SubmitField, validators

import sqlite3


class RegisterForm(FlaskForm):
    """
    Flask Form to register a new driver into the database.
    """
    # All inputs in a register form.

    # # ID
    driver_id = StringField('ID',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=9, max=9)])

    # # Name
    driver_name = StringField('Name',
                              validators=[validators.InputRequired()])

    # # Date Of Birth
    driver_dob = DateField('Date Of Birth',
                           format='%Y-%m-%d',
                           validators=[validators.InputRequired()])

    # # Hire Date
    driver_hire_date = DateField('Hire Date',
                                 format='%Y-%m-%d',
                                 validators=[validators.InputRequired()])

    # # Address
    driver_address_block_number = IntegerField('Block/House Number', validators=[validators.InputRequired()])
    driver_address_unit_floor_number = IntegerField('Unit Floor', validators=[validators.Optional(), validators.NumberRange(min=1, max=50)])
    driver_address_unit_apartment_number = IntegerField('Apartment Number', validators=[validators.Optional()])
    driver_address_street = StringField('Street', validators=[validators.InputRequired()])
    driver_address_postal_code = IntegerField('Postal Code', validators=[validators.InputRequired(), validators.NumberRange(min=100000, max=999999)])

    # # Plate Number
    driver_plate_number = StringField('Plate Number',
                                      validators=[validators.InputRequired()])

    # # Email
    driver_email = EmailField('Email',
                              validators=[validators.InputRequired()])

    # # Password
    driver_new_password = PasswordField('New Password',
                                        validators=[validators.InputRequired(),
                                                    validators.Length(min=8)])
    driver_confirm_password = PasswordField('Confirm Password',
                                            validators=[validators.EqualTo('driver_new_password')])

    # # Submit
    form_submit = SubmitField('Register')

    # Validators
    def validate_driver_id(self, driver_id_field):  # Check that the driver has not existed.
        with sqlite3.connect("grab_locator.db") as db:
            cursor = db.cursor()
            cursor.execute("""
                           SELECT * FROM DRIVER WHERE driver_id=?
                           """, (driver_id_field.data,))
            if cursor.fetchone():
                raise validators.ValidationError("You have already registered!")

    def validate_dob(self, driver_dob_field):  # Check age is between 21 to 69.
        age = (date.today() - driver_dob_field.data) // timedelta(days=365.2425)
        if age < 21 or age > 69:
            raise validators.ValidationError("Age should be between 21 to 69 years old.")

    def validate_hire_date(self, driver_hire_date_field):  # Check the hire date is after the dob.
        if driver_hire_date_field.data < self.driver_dob.data:
            raise validators.ValidationError("Hire date must be after date of birth.")


class LoginForm(FlaskForm):
    """
    Flask Form to log an existing driver in.
    """
    # All inputs in a login form.
    driver_id = StringField('ID',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=9, max=9)])
    driver_password = PasswordField('Password',
                                    validators=[validators.InputRequired()])
    form_submit = SubmitField('Login')
