import psycopg2
from psycopg2.extras import DictCursor
import time

while True:
    try:
        # Connect to your postgres DB
        postgres_connection = psycopg2.connect(
            database="fastapi",
            user="postgres",
            password="passwd",
            cursor_factory=DictCursor,
        )

        # Open a cursor to perform database operations
        postgres_cursor = postgres_connection.cursor()
        print("Postgress connected")
        break

    except Exception as error:
        print("Postgres connection failed")
        print("Error: ", error)
        time.sleep(2)

# Execute a query
postgres_cursor.execute("SELECT * FROM posts")

# Retrieve query results
records = postgres_cursor.fetchall()
