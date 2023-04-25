import sqlite3

# Connect to the database
conn = sqlite3.connect('login.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE login_detail
             (identity text, password text)''')

# Insert data into the table
cursor.execute("INSERT INTO login_detail VALUES ('98708072002','testing1')")
cursor.execute("INSERT INTO login_detail VALUES ('98704101997','testing2')")
cursor.execute("INSERT INTO login_detail VALUES ('98701012001','testing3')")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
