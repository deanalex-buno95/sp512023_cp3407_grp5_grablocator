import sqlite3
from address import Address

con = sqlite3.connect('address.db')

c = con.cursor()

c.execute(''' CREATE TABLE address(
        blk_num integer
        street_num integer 
        unit_num integer 
        postal_code integer 
    )''')


con.commit()

con.close()