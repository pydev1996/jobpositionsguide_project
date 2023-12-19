import sqlite3
import mysql.connector

# Connect to SQLite database
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL database
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aleesha#143',
    database='careerpath'
)
mysql_cursor = mysql_conn.cursor()

# Define the table name in SQLite
sqlite_table_name = 'jobpositions_jobposition'

# Fetch data from SQLite
sqlite_cursor.execute(f'SELECT * FROM {sqlite_table_name}')
sqlite_data = sqlite_cursor.fetchall()

# Define the table name in MySQL
mysql_table_name = 'jobpositions_jobposition'

# Insert data into MySQL
for row in sqlite_data:
    mysql_cursor.execute(f"INSERT INTO {mysql_table_name} (column1, column2, column3, ...) VALUES (%s, %s, %s, ...)", row)

# Commit changes and close connections
mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()
