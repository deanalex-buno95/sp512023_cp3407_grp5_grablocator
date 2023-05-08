"""
Flask App file

app.py
"""

from flask import Flask, redirect, render_template, session, url_for
import sqlite3

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "c2e3QoE'Ug)C--xJ(SHu?+R+9bd^ap"

db = sqlite3.connect("grab_locator.db")
cursor = db.cursor()

"""
All Functions
"""


def add_new_address(address_block_number,
                    address_unit_floor_number,
                    address_unit_apartment_number,
                    address_street,
                    driver_address_postal_code):
    """
    Add a new address.
    :param address_block_number: int
    :param address_unit_floor_number: int
    :param address_unit_apartment_number: int
    :param address_street: str
    :param driver_address_postal_code: str
    """
    address_id = str(driver_address_postal_code)
    if address_unit_floor_number is not None and address_unit_apartment_number is not None:
        address_id += f"|{address_unit_floor_number}-{address_unit_apartment_number}"
    address_row = (address_id, address_block_number, address_unit_floor_number, address_unit_apartment_number,
                   address_street, driver_address_postal_code)
    address_query = """
                    INSERT INTO ADDRESS (address_id, address_block_number,
                    address_unit_floor_number, address_unit_apartment_number,
                    address_street, address_postal_code)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
    cursor.execute(address_query, address_row)
    db.commit()


def add_new_driver(driver_id, driver_name,
                   driver_dob, driver_hire_date,
                   driver_plate_number, driver_email, driver_password):
    """
    Register a new driver, along with its addresses.
    :param driver_id: str
    :param driver_name: str
    :param driver_dob: date
    :param driver_hire_date: date
    :param driver_plate_number: str
    :param driver_email: str
    :param driver_password: str
    """
    driver_row = (driver_id, driver_name, driver_dob, driver_hire_date, driver_plate_number, driver_email,
                  driver_password)
    driver_query = """
                   INSERT INTO DRIVER (driver_id, driver_name,
                   driver_dob, driver_hire_date,
                   driver_plate_number, driver_email, driver_password)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   """
    cursor.execute(driver_query, driver_row)
    db.commit()


def add_new_driveraddress(driveraddress_driver_id, driveraddress_address_id):
    """
    Add an instance of the composite element containing the IDs of the Driver and Address.
    :param driveraddress_driver_id: str
    :param driveraddress_address_id: str
    """
    driveraddress_row = (driveraddress_driver_id, driveraddress_address_id)
    driveraddress_query = """
                          INSERT INTO DRIVERADDRESS (driveraddress_driver_id, driveraddress_address_id)
                          VALUES (?, ?)
                          """
    cursor.execute(driveraddress_query, driveraddress_row)
    db.commit()


"""
All Routes
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        driver_id = form.driver_id.data.upper()
        driver_password = form.driver_password.data
        session['logged_in'] = True
        session['driver_id'] = driver_id
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        driver_id = form.driver_id.data
        driver_name = form.driver_name.data
        driver_dob = form.driver_dob.data
        driver_hire_date = form.driver_hire_date.data
        driver_address_block_number = form.driver_address_block_number.data
        driver_address_unit_floor_number = form.driver_address_unit_floor_number.data
        driver_address_unit_apartment_number = form.driver_address_unit_apartment_number.data
        driver_address_street = form.driver_address_street
        driver_address_postal_code = form.driver_address_postal_code.data
        driver_plate_number = form.driver_plate_number.data
        driver_email = form.driver_email.data.lower()
        driver_password = form.driver_confirm_password.data
        session['logged_in'] = True
        session['driver_id'] = driver_id
        return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/')
def index():
    if 'logged_in' in session:
        driver_id = session['driver_id']
        return render_template("index.html", driver_id=driver_id)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('driver_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))


app.run(debug=True)
db.close()
