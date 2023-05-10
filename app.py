"""
Flask App file

app.py
"""

from flask import Flask, redirect, render_template, session, url_for
import sqlite3

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "c2e3QoE'Ug)C--xJ(SHu?+R+9bd^ap"

"""
All Functions
"""


def create_address_id(address_postal_code, address_unit_floor_number=None, address_unit_apartment_number=None):
    """
    Create the address ID.
    :param address_postal_code: int
    :param address_unit_floor_number: int
    :param address_unit_apartment_number: int
    :return: str
    """
    address_id = str(address_postal_code)
    if address_unit_floor_number is not None and address_unit_apartment_number is not None:
        address_id += f"|{address_unit_floor_number:02d}-{address_unit_apartment_number}"
    return address_id


def add_data_query(query, data_row):
    """
    Add data.
    :param query: str
    :param data_row:
    :return:
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    cursor.execute(query, data_row)
    connection.commit()
    connection.close()


def get_correct_password(driver_id):
    """
    Get correct password from the driver ID.
    :param driver_id: str
    :return: str
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    query = """
            SELECT driver_password FROM DRIVER
            WHERE driver_id = ?
            """
    data_row = (driver_id,)
    cursor.execute(query, data_row)
    driver_password_tuple = cursor.fetchone()
    connection.close()
    return driver_password_tuple[0]


def get_driver_name_from_driver_id(driver_id):
    """
    Get driver's name of the person based on his/her driver ID.
    :param driver_id: str
    :return: str
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    query = """
            SELECT driver_name FROM DRIVER
            WHERE driver_id = ?
            """
    data_row = (driver_id,)
    cursor.execute(query, data_row)
    driver_name_tuple = cursor.fetchone()
    connection.close()
    return driver_name_tuple[0]


"""
All Routes
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Fields data.
        driver_id = form.driver_id.data
        driver_password = form.driver_password.data

        # Get correct password, or lack thereof.
        driver_correct_password = get_correct_password(driver_id)

        # If password is correct.
        if driver_password == driver_correct_password:
            session['logged_in'] = True
            session['driver_id'] = driver_id
            return redirect(url_for('index'))
        else:
            print("Password incorrect!")
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Fields data.
        driver_id = form.driver_id.data
        driver_name = form.driver_name.data
        driver_dob = form.driver_dob.data
        driver_hire_date = form.driver_hire_date.data
        driver_address_block_number = form.driver_address_block_number.data
        driver_address_unit_floor_number = form.driver_address_unit_floor_number.data
        driver_address_unit_apartment_number = form.driver_address_unit_apartment_number.data
        driver_address_street = form.driver_address_street.data
        driver_address_postal_code = form.driver_address_postal_code.data
        driver_plate_number = form.driver_plate_number.data
        driver_email = form.driver_email.data.lower()
        driver_password = form.driver_confirm_password.data

        # Data rows.
        address_id = create_address_id(driver_address_postal_code, driver_address_unit_floor_number,
                                       driver_address_unit_apartment_number)
        address_row = (address_id, driver_address_block_number, driver_address_unit_floor_number,
                       driver_address_unit_apartment_number, driver_address_street, driver_address_postal_code)

        driver_row = (driver_id, driver_name, driver_dob, driver_hire_date, driver_plate_number, driver_email,
                      driver_password)

        driveraddress_row = (driver_id, address_id)

        # Queries.
        address_query = """
                        INSERT INTO ADDRESS (address_id, address_block_number, address_unit_floor_number,
                        address_unit_apartment_number, address_street, address_postal_code)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """

        driver_query = """
                       INSERT INTO DRIVER (driver_id, driver_name, driver_dob, driver_hire_date, driver_plate_number,
                       driver_email, driver_password)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """

        driveraddress_query = """
                              INSERT INTO DRIVERADDRESS (driveraddress_driver_id, driveraddress_address_id)
                              VALUES (?, ?)
                              """

        # Apply queries on data.
        all_queries_fulfilled = True
        for query, data_row in [(address_query, address_row), (driver_query, driver_row),
                                (driveraddress_query, driveraddress_row)]:
            try:
                add_data_query(query, data_row)
            except Exception as e:
                print(f"An error occurred for {(query, data_row)}: {e}")
                all_queries_fulfilled = False

        # Sessions.
        if all_queries_fulfilled:
            session['logged_in'] = True
            session['driver_id'] = driver_id
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/')
def index():
    if 'logged_in' in session:
        driver_id = session['driver_id']
        driver_name = get_driver_name_from_driver_id(driver_id).title()
        return render_template("index.html", driver_name=driver_name)
    else:
        return redirect(url_for('login'))


@app.route('/orders')
def orders():
    if 'logged_in' in session:
        return render_template("orders.html")
    else:
        return redirect(url_for('login'))


@app.route('/history')
def history():
    if 'logged_in' in session:
        return render_template("history.html")
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    if 'logged_in' in session:
        return render_template("about.html")
    else:
        return redirect(url_for('login'))


@app.route('/contact')
def contact():
    if 'logged_in' in session:
        return render_template("contact.html")
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('driver_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))


app.run(debug=True)
