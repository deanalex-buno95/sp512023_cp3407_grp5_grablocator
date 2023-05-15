"""
All forms needed for our website – GrabLocator

forms.py
"""


from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, SubmitField, validators

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
    driver_address_block_number = StringField('Block/House Number', validators=[validators.InputRequired(),
                                                                                validators.Regexp('^[0-9a-zA-Z]*$',
                                                                                                  message='Field must contain only letters and numbers')])
    driver_address_unit_number = StringField('Unit Number', validators=[validators.Optional()])
    driver_address_street = StringField('Street', validators=[validators.InputRequired()])
    driver_address_postal_code = StringField('Postal Code', validators=[validators.InputRequired(),
                                                                        validators.Length(min=6, max=6),
                                                                        validators.Regexp('^[0-9]*$',
                                                                                          message='Field must contain only numbers')])

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

    # To uppercase
    def to_uppercase(self, field):
        field.data = field.data.upper()

    # Validators
    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        self.to_uppercase(self.driver_id)
        self.to_uppercase(self.driver_name)
        self.to_uppercase(self.driver_address_block_number)
        self.to_uppercase(self.driver_address_street)
        self.to_uppercase(self.driver_plate_number)
        return True

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

    # To uppercase
    def to_uppercase(self, field):
        field.data = field.data.upper()

    # Validators
    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        self.to_uppercase(self.driver_id)
        return True

    def validate_driver_id_and_password(self,
                                        driver_id_field, driver_password_field):  # Check right driver and password.
        with sqlite3.connect("grab_locator.db") as db:
            cursor = db.cursor()
            cursor.execute("""
                           SELECT driver_id, driver_password FROM DRIVER WHERE driver_id=?
                           """, (driver_id_field.data,))
            result = cursor.fetchone()
            if not result:  # No results.
                raise validators.ValidationError("You have not registered!")
            elif result[1] != driver_password_field.data:  # Incorrect password.
                raise validators.ValidationError("The password is incorrect!")
            db.close()
