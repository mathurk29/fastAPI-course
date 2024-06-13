# wait_for.py
import os
import time
import psycopg2
from urllib.parse import urlparse

RETRIES = 15

parsed_url = urlparse(os.getenv("DATABASE_URL"))
print(f"parsed_url: {parsed_url}")
while RETRIES:
    try:
        conn = psycopg2.connect(
            dbname=parsed_url.path[1:],
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port,
        )
        print(f'Connected to {parsed_url}')
        conn.close()
        break
    except psycopg2.OperationalError:
        RETRIES -= 1
        time.sleep(5)
