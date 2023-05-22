"""
Flask App file

app.py
"""

from flask import Flask, redirect, render_template, session, url_for
import sqlite3

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "c2e3QoE'Ug)C--xJ(SHu?+R+9bd^ap"

EXPERIENCED_QUOTA = 5
VERY_EXPERIENCED_QUOTA = 8
MINIMUM_OLD_AGE = 50

"""
All Functions
"""


def create_address_id(address_postal_code, address_unit_number=None):
    """
    Create the address ID.
    :param address_postal_code: int
    :param address_unit_number: str
    :return: str
    """
    address_id = str(address_postal_code)
    if address_unit_number is not None:
        address_id += f"|{address_unit_number}"
    return address_id


def add_data_query(query, data_row):
    """
    Add data.
    :param query: str
    :param data_row: tuple
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
    Get driver's nam based on his/her driver ID.
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


def get_driver_postal_code_from_driver_id(driver_id):
    """
    Get driver's postal code based on his/her driver ID.
    :param driver_id: str
    :return: str
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    query = """
            SELECT address_postal_code FROM ADDRESS, DRIVERADDRESS, DRIVER
            WHERE DRIVER.driver_id = DRIVERADDRESS.driveraddress_driver_id
            AND DRIVERADDRESS.driveraddress_address_id = ADDRESS.address_id
            AND DRIVER.driver_id = ?
            """
    data_row = (driver_id,)
    cursor.execute(query, data_row)
    driver_name_tuple = cursor.fetchone()
    connection.close()
    return driver_name_tuple[0]


def get_nearest_station_code_from_postal_sector(postal_sector):
    """
    Get the nearest station code from the postal sector.
    :param postal_sector: str
    :return: str
    """
    station_to_postal_sectors_dictionary = {"ST01": ("01", "02", "03", "04", "05", "06"),
                                            "ST02": ("07", "08"),
                                            "ST03": ("14", "15", "16"),
                                            "ST04": ("09", "10"),
                                            "ST05": ("11", "12", "13"),
                                            "ST06": ("17",),
                                            "ST07": ("18", "19"),
                                            "ST08": ("20", "21"),
                                            "ST09": ("22", "23"),
                                            "ST10": ("24", "25", "26", "27"),
                                            "ST11": ("28", "29", "30"),
                                            "ST12": ("31", "32", "33"),
                                            "ST13": ("34", "35", "36", "37"),
                                            "ST14": ("38", "39", "40", "41"),
                                            "ST15": ("42", "43", "44", "45"),
                                            "ST16": ("46", "47", "48"),
                                            "ST17": ("49", "50", "81"),
                                            "ST18": ("51", "52"),
                                            "ST19": ("53", "54", "55", "82"),
                                            "ST20": ("56", "57"),
                                            "ST21": ("58", "59"),
                                            "ST22": ("60", "61", "62", "63", "64"),
                                            "ST23": ("65", "66", "67", "68"),
                                            "ST24": ("69", "70", "71", "72", "73"),
                                            "ST25": ("77", "78"),
                                            "ST26": ("75", "76"),
                                            "ST27": ("79", "80")}
    for station in station_to_postal_sectors_dictionary:
        if postal_sector in station_to_postal_sectors_dictionary[station]:
            return station


def get_available_orders_of_driver(driver_postal_sector, driver_nearest_station_code):
    """
    Get available orders of the driver.
    :param driver_postal_sector: str
    :param driver_nearest_station_code: str
    :return: list
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    available_orders_query = """
                             SELECT graborder_id, PickupDestAddress.address_block_number,
                             PickupDestAddress.address_unit_number, PickupDestAddress.address_street,
                             PickupDestAddress.address_postal_code, FinalDestAddress.address_block_number,
                             FinalDestAddress.address_unit_number, FinalDestAddress.address_street,
                             FinalDestAddress.address_postal_code
                             FROM GRABORDER, ADDRESS PickupDestAddress, ADDRESS FinalDestAddress
                             JOIN PICKUPDEST ON GRABORDER.graborder_pickupdest_id = PICKUPDEST.pickupdest_id
                             JOIN FINALDEST ON GRABORDER.graborder_finaldest_id = FINALDEST.finaldest_id
                             JOIN DESTINATION PickupD ON PICKUPDEST.pickupdest_id = PickupD.dest_address_id
                             JOIN DESTINATION FinalD ON FINALDEST.finaldest_id = FinalD.dest_address_id
                             WHERE graborder_driver_id IS NULL
                             AND PickupD.dest_address_id = PickupDestAddress.address_id
                             AND FinalD.dest_address_id = FinalDestAddress.address_id
                             AND (PickupDestAddress.address_postal_code LIKE ? OR PickupDestAddress.address_id = ?)
                             """
    available_orders_data = (f"{driver_postal_sector}%", driver_nearest_station_code)
    cursor.execute(available_orders_query, available_orders_data)
    available_orders = cursor.fetchall()
    connection.close()
    return available_orders


def get_pending_orders_of_driver(driver_id):
    """
    Get pending orders of the driver.
    :param driver_id: str
    :return: list
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    pending_orders_query = """
                           SELECT graborder_id, PickupDestAddress.address_block_number,
                           PickupDestAddress.address_unit_number, PickupDestAddress.address_street,
                           PickupDestAddress.address_postal_code, FinalDestAddress.address_block_number,
                           FinalDestAddress.address_unit_number, FinalDestAddress.address_street,
                           FinalDestAddress.address_postal_code
                           FROM GRABORDER, ADDRESS PickupDestAddress, ADDRESS FinalDestAddress
                           JOIN PICKUPDEST ON GRABORDER.graborder_pickupdest_id = PICKUPDEST.pickupdest_id
                           JOIN FINALDEST ON GRABORDER.graborder_finaldest_id = FINALDEST.finaldest_id
                           JOIN DESTINATION PickupD ON PICKUPDEST.pickupdest_id = PickupD.dest_address_id
                           JOIN DESTINATION FinalD ON FINALDEST.finaldest_id = FinalD.dest_address_id
                           WHERE PickupD.dest_address_id = PickupDestAddress.address_id
                           AND FinalD.dest_address_id = FinalDestAddress.address_id
                           AND graborder_driver_id = ?
                           """
    pending_orders_data = (driver_id,)
    cursor.execute(pending_orders_query, pending_orders_data)
    pending_orders = cursor.fetchall()
    connection.close()
    return pending_orders


def get_current_order(order_id):
    """
    Get order currently in the selected order page.
    :param order_id: str
    :return: list
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    current_order_query = """
                          SELECT PickupDestAddress.address_id, PickupD.dest_name,
                          PickupDestAddress.address_block_number, PickupDestAddress.address_unit_number, 
                          PickupDestAddress.address_street, PickupDestAddress.address_postal_code,
                          FinalDestAddress.address_id, FinalD.dest_name,
                          FinalDestAddress.address_block_number, FinalDestAddress.address_unit_number,
                          FinalDestAddress.address_street, FinalDestAddress.address_postal_code,
                          (
                              IF (graborder_driver_id IS NOT NULL, 1, 0)
                          ) AS 'is_pending'
                          FROM GRABORDER, ADDRESS PickupDestAddress, ADDRESS FinalDestAddress
                          JOIN PICKUPDEST ON GRABORDER.graborder_pickupdest_id = PICKUPDEST.pickupdest_id
                          JOIN FINALDEST ON GRABORDER.graborder_finaldest_id = FINALDEST.finaldest_id
                          JOIN DESTINATION PickupD ON PICKUPDEST.pickupdest_id = PickupD.dest_address_id
                          JOIN DESTINATION FinalD ON FINALDEST.finaldest_id = FinalD.dest_address_id
                          WHERE PickupD.dest_address_id = PickupDestAddress.address_id
                          AND FinalD.dest_address_id = FinalDestAddress.address_id
                          AND graborder_id = ?
                          """
    current_order_data = (order_id,)
    cursor.execute(current_order_query, current_order_data)
    current_order = cursor.fetchone()
    connection.close()
    return current_order


def get_full_address_string(name, block_number, unit_number, street, postal_code):
    """
    Get the full address string with the necessary fields.
    :param name: str
    :param block_number: str
    :param unit_number: str
    :param street: str
    :param postal_code: str
    :return: str
    """
    return f"{f'{name}, ' if name else ''}Block {block_number}{f', #{unit_number}' if unit_number else ''}, {street.title()}, Singapore {postal_code}"


def get_order_from_station_is_intersector(station_id, final_destination_postal_code):
    """
    Check if the order that starts from a station is intersectional.
    :param station_id: str
    :param final_destination_postal_code: str
    :return: bool
    """
    station_to_postal_sectors_dictionary = {"ST01": ("01", "02", "03", "04", "05", "06"),
                                            "ST02": ("07", "08"),
                                            "ST03": ("14", "15", "16"),
                                            "ST04": ("09", "10"),
                                            "ST05": ("11", "12", "13"),
                                            "ST06": ("17",),
                                            "ST07": ("18", "19"),
                                            "ST08": ("20", "21"),
                                            "ST09": ("22", "23"),
                                            "ST10": ("24", "25", "26", "27"),
                                            "ST11": ("28", "29", "30"),
                                            "ST12": ("31", "32", "33"),
                                            "ST13": ("34", "35", "36", "37"),
                                            "ST14": ("38", "39", "40", "41"),
                                            "ST15": ("42", "43", "44", "45"),
                                            "ST16": ("46", "47", "48"),
                                            "ST17": ("49", "50", "81"),
                                            "ST18": ("51", "52"),
                                            "ST19": ("53", "54", "55", "82"),
                                            "ST20": ("56", "57"),
                                            "ST21": ("58", "59"),
                                            "ST22": ("60", "61", "62", "63", "64"),
                                            "ST23": ("65", "66", "67", "68"),
                                            "ST24": ("69", "70", "71", "72", "73"),
                                            "ST25": ("77", "78"),
                                            "ST26": ("75", "76"),
                                            "ST27": ("79", "80")}
    return True if final_destination_postal_code[:2] not in station_to_postal_sectors_dictionary[station_id] else False


def get_age_and_experience_of_driver(driver_id):
    """
    Get the age and experience of the driver.
    :param driver_id: str
    :return: tuple
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    driver_age_and_experience_query = """
                                      SELECT
                                      strftime('%Y', 'now') - strftime('%Y', driver_dob) -
                                      (strftime('%m-%d', 'now') < strftime('%m-%d', driver_dob)),
                                      strftime('%Y', 'now') - strftime('%Y', driver_hire_date) -
                                      (strftime('%m-%d', 'now') < strftime('%m-%d', driver_hire_date))
                                      FROM DRIVER
                                      WHERE driver_id = ?
                                      """
    driver_age_and_experience_data = (driver_id,)
    cursor.execute(driver_age_and_experience_query, driver_age_and_experience_data)
    driver_age_and_experience = cursor.fetchone()
    connection.close()
    return driver_age_and_experience


def get_stopping_point_address(stopping_point_id):
    """
    Get address of the stopping point chosen.
    :param stopping_point_id: str
    :return: str
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    stopping_point_address_query = """
                                   SELECT
                                   dest_name, address_block_number, address_unit_number, address_street,
                                   address_postal_code
                                   FROM ADDRESS, DESTINATION
                                   WHERE ADDRESS.address_id = DESTINATION.dest_address_id
                                   AND ADDRESS.address_id = ?
                                   """
    stopping_point_address_data = (stopping_point_id,)
    cursor.execute(stopping_point_address_query, stopping_point_address_data)
    stopping_point_address = cursor.fetchone()
    connection.close()
    stopping_point_address_string = get_full_address_string(stopping_point_address[0],
                                                            stopping_point_address[1],
                                                            stopping_point_address[2],
                                                            stopping_point_address[3],
                                                            stopping_point_address[4])
    return stopping_point_address_string


def get_driver_history_list(driver_id):
    """
    Get the driver's history of locations explored.
    :param driver_id: str
    :return: list
    """
    connection = sqlite3.connect("grab_locator.db")
    cursor = connection.cursor()
    driver_history_list_query = """
                                SELECT
                                dest_name, address_block_number, address_unit_number, address_street,
                                address_postal_code, driverdest_date
                                FROM DRIVERDEST, DESTINATION, ADDRESS
                                JOIN DRIVER ON DRIVER.driver_id = DRIVERDEST.driverdest_driver_id
                                WHERE DRIVERDEST.driverdest_dest_address_id = DESTINATION.dest_address_id
                                AND DESTINATION.dest_address_id = ADDRESS.address_id
                                AND DRIVER.driver_id = ?
                                """
    driver_history_list_data = (driver_id,)
    cursor.execute(driver_history_list_query, driver_history_list_data)
    driver_history_list_temp = cursor.fetchall()
    driver_history_list = []
    for driver_history in driver_history_list_temp:
        driver_history_address = get_full_address_string(driver_history[0],
                                                         driver_history[1],
                                                         driver_history[2],
                                                         driver_history[3],
                                                         driver_history[4])
        driver_history_list.append((driver_history_address, driver_history[5]))
    connection.close()
    return driver_history_list


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
        driver_address_unit_number = form.driver_address_unit_number.data
        driver_address_street = form.driver_address_street.data
        driver_address_postal_code = form.driver_address_postal_code.data
        driver_plate_number = form.driver_plate_number.data
        driver_email = form.driver_email.data.lower()
        driver_password = form.driver_confirm_password.data

        # Data rows.
        address_id = create_address_id(driver_address_postal_code, driver_address_unit_number)
        address_row = (address_id, driver_address_block_number, driver_address_unit_number, driver_address_street,
                       driver_address_postal_code)

        driver_row = (driver_id, driver_name, driver_dob, driver_hire_date, driver_plate_number, driver_email,
                      driver_password)

        driveraddress_row = (driver_id, address_id)

        # Queries.
        address_query = """
                        INSERT INTO ADDRESS (address_id, address_block_number, address_unit_number, address_street,
                        address_postal_code)
                        VALUES (?, ?, ?, ?, ?)
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
        # Take driver ID.
        driver_id = session['driver_id']

        # Get driver name.
        driver_name = get_driver_name_from_driver_id(driver_id).title()

        return render_template("index.html", driver_name=driver_name)

    else:
        return redirect(url_for('login'))


@app.route('/orders')
def orders():
    if 'logged_in' in session:
        # Take driver ID.
        driver_id = session['driver_id']

        # Get all needed information.
        driver_postal_code = get_driver_postal_code_from_driver_id(driver_id)
        driver_postal_sector = driver_postal_code[:2]
        driver_nearest_station_code = get_nearest_station_code_from_postal_sector(driver_postal_sector)
        available_orders = get_available_orders_of_driver(driver_postal_sector, driver_nearest_station_code)
        pending_orders = get_pending_orders_of_driver(driver_id)

        return render_template("orders.html", available_orders=available_orders, pending_orders=pending_orders)
    else:
        return redirect(url_for('login'))


@app.route('/selectedorder/<string:order_id>')
def selectedorder(order_id):
    if 'logged_in' in session:
        # Take driver ID.
        driver_id = session['driver_id']

        # Get current order and its status.
        current_order = get_current_order(order_id)
        is_pending = bool(current_order[-1])

        # Get the pickup destination.
        pickup_destination_id = current_order[0]
        pickup_destination_name = current_order[1]
        pickup_destination_block_number = current_order[2]
        pickup_destination_unit_number = current_order[3]
        pickup_destination_street = current_order[4]
        pickup_destination_postal_code = current_order[5]
        pickup_destination_address_string = get_full_address_string(pickup_destination_name,
                                                                    pickup_destination_block_number,
                                                                    pickup_destination_unit_number,
                                                                    pickup_destination_street,
                                                                    pickup_destination_postal_code)

        # Get the final destination.
        final_destination_id = current_order[6]
        final_destination_name = current_order[7]
        final_destination_block_number = current_order[8]
        final_destination_unit_number = current_order[9]
        final_destination_street = current_order[10]
        final_destination_postal_code = current_order[11]
        final_destination_address_string = get_full_address_string(final_destination_name,
                                                                   final_destination_block_number,
                                                                   final_destination_unit_number,
                                                                   final_destination_street,
                                                                   final_destination_postal_code)

        # Check if the order is intra- or inter-sector.
        if pickup_destination_id[:2] == "ST":  # Is a station.
            order_is_intersector = get_order_from_station_is_intersector(pickup_destination_id,
                                                                         final_destination_postal_code)
        else:  # Is not a station.
            order_is_intersector = (pickup_destination_postal_code[:2] != final_destination_postal_code[
                                                                          :2])  # Check that the postal sectors are different.

        # Age and experience.
        age, experience = get_age_and_experience_of_driver(driver_id)

        # Determine where should the driver stop after winning.
        if order_is_intersector:  # Inter-sector
            if pickup_destination_id[:2] == "ST":  # Is a station, start from closest station to pickup.
                if age < MINIMUM_OLD_AGE and experience >= EXPERIENCED_QUOTA:  # Go to final destination.
                    stopping_point_id = final_destination_id
                else:  # Go to the station that is closest to the final destination.
                    stopping_point_id = get_nearest_station_code_from_postal_sector(final_destination_id[:2])
            else:  # Is not a station, start from pickup.
                if age < MINIMUM_OLD_AGE and experience >= EXPERIENCED_QUOTA:  # At minimum, go to the other sector.
                    stopping_point_id = get_nearest_station_code_from_postal_sector(final_destination_id[:2])
                    if experience >= VERY_EXPERIENCED_QUOTA:  # Overwrite if the person is very experienced.
                        stopping_point_id = final_destination_id
                else:  # Go to the station nearest to the pickup.
                    stopping_point_id = get_nearest_station_code_from_postal_sector(pickup_destination_id[:2])
        else:  # Intra-sector
            if pickup_destination_id[:2] == "ST":  # Is a station.
                stopping_point_id = final_destination_id
            else:  # Is not a station.
                if age < MINIMUM_OLD_AGE and experience >= EXPERIENCED_QUOTA:
                    stopping_point_id = final_destination_id
                else:  # Is not a station.
                    stopping_point_id = get_nearest_station_code_from_postal_sector(final_destination_id[:2])
        print(stopping_point_id)

        # Get the address of the new stopping point.
        stopping_point_address = get_stopping_point_address(stopping_point_id)

        return render_template("selectedorder.html", order_id=order_id,
                               pickup_destination_address_string=pickup_destination_address_string,
                               final_destination_address_string=final_destination_address_string,
                               is_pending=is_pending,
                               stopping_point_address=stopping_point_address)
    else:
        return redirect(url_for('login'))


@app.route('/history')
def history():
    if 'logged_in' in session:
        driver_id = session['driver_id']
        driver_history_list = get_driver_history_list(driver_id)
        return render_template("history.html", driver_history_list=driver_history_list)
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
