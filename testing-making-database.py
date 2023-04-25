import sqlite3
from login import Login

conn = sqlite3.connect('login.db')


cursor = conn.cursor()

# cursor.execute('''CREATE TABLE login
#              (identity integer ,
#              password text)
#              ''')
#
# cursor.execute("INSERT INTO login VALUES (98708072002,'testing1')")
# cursor.execute("INSERT INTO login VALUES (98704101997,'testing2')")
# cursor.execute("INSERT INTO login VALUES (98701012001,'testing3')")

cursor.execute("SELECT * FROM login WHERE identity='98704101097'")

print(cursor.fetchone())

conn.commit()

conn.close()
