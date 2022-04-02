import sqlite3

with sqlite3.connect('database') as connection:
    connection.execute('INSERT INTO Users')