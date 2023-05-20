"""
Add stations into DB.

add_stations.py
"""


import csv
import sqlite3


def execute_query(query, data_row):
    """
    Execute query to add station data into the necessary tables.
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
    row_number = 0  # header row
    with open('../csv/stations.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if row_number:  # data row
                print(row)  # Initial test to check row.

                # Get the station data.
                station_id = row[0]
                station_name = row[1].upper()
                station_address_block_number = row[2].upper()
                station_address_street = row[3].upper()
                station_address_postal_code = row[4][1:]

                # Proceed to write the necessary data for the queries.
                station_address = (station_id, station_address_block_number, station_address_street,
                                   station_address_postal_code)
                station_destination = (station_id, station_name)
                station_pickupdest = (station_id, True)

                # Create the queries.
                station_address_query = """
                                        INSERT INTO ADDRESS (address_id, address_block_number, address_street,
                                        address_postal_code)
                                        VALUES (?, ?, ?, ?)
                                        """
                station_destination_query = """
                                            INSERT INTO DESTINATION (dest_address_id, dest_name)
                                            VALUES (?, ?)
                                            """
                station_pickupdest_query = """
                                           INSERT INTO PICKUPDEST (pickupdest_id, pickupdest_is_station)
                                           VALUES (?, ?)
                                           """

                # Execute all queries.
                execute_query(station_address_query, station_address)
                execute_query(station_destination_query, station_destination)
                execute_query(station_pickupdest_query, station_pickupdest)

            row_number += 1
