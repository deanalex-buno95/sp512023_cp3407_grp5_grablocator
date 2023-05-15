"""
Add orders into DB.

add_orders.py
"""


import csv
import sqlite3


if __name__ == '__main__':
    row_number = 0
    with open('../csv/orders.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if row_number:
                print(row)  # Initial test to check row.

                # Get the order data.
                order_id = row[0]
                order_pickupdest_name = row[1] if row[1] is not '' else None
                order_pickupdest_address_block_number = row[2]
                order_pickupdest_address_unit_number = row[3] if row[3] is not '' else None
                order_pickupdest_address_street = row[4]
                order_pickupdest_address_postal_code = row[5]
                order_pickupdest_name = row[6] if row[6] is not '' else None
                order_pickupdest_address_block_number = row[7]
                order_pickupdest_address_unit_number = row[8] if row[8] is not '' else None
                order_pickupdest_address_street = row[9]
                order_pickupdest_address_postal_code = row[10]
                order_date = row[11]

                # Proceed to write the necessary data for the queries.

            row_number += 1
