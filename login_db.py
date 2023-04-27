import sqlite3
from login import Login


con = sqlite3.connect('login.db')

c = con.cursor()

c.execute('''CREATE TABLE login  (
            first_name text
            last_name text
            work_experience integer 
            id integer 
            password text''')

c.execute("INSERT INTO login ('John', 'Doe', '2', '98701012001', 'Testing1')")
c.execute("INSERT INTO login ('Jane', 'Doe', '5', '98702012001', 'Testing2')")
c.execute("INSERT INTO login ('Ja', 'Doe', '8', '98703012001', 'Testing3')")
c.execute("INSERT INTO login ('James', 'Doe', '11', '98704012001', 'Testing4')")

con.commit()

con.close()

