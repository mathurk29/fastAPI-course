import psycopg2
from psycopg2.extras import DictCursor

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
        database="fastapi", user="postgres", password="passwd", cursor_factory=DictCursor
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    print("Postgress connected")

except Exception as error:
    print("Postgres connection failed")
    print("Error: ", error)

# Execute a query
cur.execute("SELECT * FROM posts")

# Retrieve query results
records = cur.fetchall()
