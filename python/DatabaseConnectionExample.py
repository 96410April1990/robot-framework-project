import sqlite3

connection = sqlite3.connect("Example.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM employees WHERE salary > 80000")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()

