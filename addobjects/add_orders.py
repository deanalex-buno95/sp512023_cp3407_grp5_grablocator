"""
Add orders into DB.

add_orders.py
"""


import csv
import sqlite3


def execute_query(query, data_row):
    """
    Execute query to add order data into the necessary tables.
    :param query: str
    :param data_row: tuple
    """
    connection = sqlite3.connect("../grab_locator.db")
    cursor = connection.cursor()
    try:
        cursor.execute(query, data_row)
    except Exception as e:
        print(f"An error occurred for {(query, data_row)}: {e}")
    else:
        print(f"{data_row} added.")
    connection.commit()
    connection.close()


if __name__ == '__main__':
    row_number = 0
    with open('../csv/orders.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if row_number:
                print(row)  # Initial test to check row.

                # Get the order data.
                order_id = row[0]
                order_pickupdest_name = row[1] if row[1] != '' else None
                order_pickupdest_address_block_number = row[2]
                order_pickupdest_address_unit_number = row[3] if row[3] != '' else None
                order_pickupdest_address_street = row[4]
                order_pickupdest_address_postal_code = row[5][1:]
                order_finaldest_name = row[6] if row[6] != '' else None
                order_finaldest_address_block_number = row[7]
                order_finaldest_address_unit_number = row[8] if row[8] != '' else None
                order_finaldest_address_street = row[9]
                order_finaldest_address_postal_code = row[10][1:]
                order_date = row[11]

                # Proceed to write the necessary data for the queries.
                order_pickupdest_address_id = f"{order_pickupdest_address_postal_code}|{order_pickupdest_address_unit_number}" if order_pickupdest_address_unit_number is not None else str(order_pickupdest_address_postal_code)
                order_pickupdest_address = (order_pickupdest_address_id, order_pickupdest_address_block_number,
                                            order_pickupdest_address_unit_number, order_pickupdest_address_street,
                                            order_pickupdest_address_postal_code)
                order_pickupdest_destination = (order_pickupdest_address_id, order_pickupdest_name)
                order_pickupdest = (order_pickupdest_address_id,)

                order_finaldest_address_id = f"{order_finaldest_address_postal_code}|{order_finaldest_address_unit_number}" if order_finaldest_address_unit_number is not None else str(order_finaldest_address_postal_code)
                order_finaldest_address = (order_finaldest_address_id, order_finaldest_address_block_number,
                                           order_finaldest_address_unit_number, order_finaldest_address_street,
                                           order_finaldest_address_postal_code)
                order_finaldest_destination = (order_finaldest_address_id, order_finaldest_name)
                order_finaldest = (order_finaldest_address_id,)

                # Create the queries.
                order_graborder = (order_id, order_pickupdest_address_id, order_finaldest_address_id, order_date)

                order_address_query = """
                                      INSERT INTO ADDRESS (address_id, address_block_number, address_unit_number,
                                      address_street, address_postal_code)
                                      VALUES (?, ?, ?, ?, ?)
                                      """
                order_destination_query = """
                                          INSERT INTO DESTINATION (dest_address_id, dest_name)
                                          VALUES (?, ?)
                                          """
                order_pickupdest_query = """
                                         INSERT INTO PICKUPDEST (pickupdest_id)
                                         VALUES (?)
                                         """
                order_finaldest_query = """
                                        INSERT INTO FINALDEST (finaldest_id)
                                        VALUES (?)
                                        """
                order_query = """
                              INSERT INTO GRABORDER (graborder_id, graborder_pickupdest_id, graborder_finaldest_id,
                              graborder_date)
                              VALUES (?, ?, ?, ?)
                              """

                # Execute all queries.
                execute_query(order_address_query, order_pickupdest_address)
                execute_query(order_address_query, order_finaldest_address)
                execute_query(order_destination_query, order_pickupdest_destination)
                execute_query(order_destination_query, order_finaldest_destination)
                execute_query(order_pickupdest_query, order_pickupdest)
                execute_query(order_finaldest_query, order_finaldest)
                execute_query(order_query, order_graborder)

            row_number += 1
