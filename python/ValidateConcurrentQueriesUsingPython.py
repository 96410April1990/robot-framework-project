import sqlite3
from concurrent.futures import ThreadPoolExecutor

def db_conn_execute_queries(order_ids):
    connection = sqlite3.connect("DBDetails.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_ids,))
    result = cursor.fetchone()
    print("Result:", result)
    connection.close()

order_ids = [1, 2, 3, 4, 5]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(db_conn_execute_queries, order_ids))

print(f"Thread result-{results}")


