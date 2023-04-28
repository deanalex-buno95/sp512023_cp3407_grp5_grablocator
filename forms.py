"""
All forms needed for our website – GrabLocator

forms.py
"""


from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, SubmitField, validators


class RegisterForm(FlaskForm):
    """
    Flask Form to register a new driver into the database.
    """
    # All inputs in a register form.
    driver_id = StringField('ID',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=9, max=9)])
    driver_name = StringField('Name',
                              validators=[validators.InputRequired()])
    driver_dob = DateField('Date Of Birth',
                           format='%Y-%m-%d',
                           validators=[validators.InputRequired()])
    driver_hire_date = DateField('Hire Date',
                                 format='%Y-%m-%d',
                                 validators=[validators.InputRequired()])
    driver_plate_number = StringField('Plate Number',
                                      validators=[validators.InputRequired()])
    driver_email = EmailField('Email',
                              validators=[validators.InputRequired()])
    driver_new_password = PasswordField('New Password',
                                        validators=[validators.InputRequired(),
                                                    validators.Length(min=8)])
    driver_confirm_password = PasswordField('Confirm Password',
                                            validators=[validators.EqualTo('driver_new_password')])
    form_submit = SubmitField('Register')

    # Validators
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
    driver_email = EmailField('Email',
                              validators=[validators.InputRequired()])
    driver_password = PasswordField('Password',
                                    validators=[validators.InputRequired()])
    form_submit = SubmitField('Login')
