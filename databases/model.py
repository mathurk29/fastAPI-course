import time

import psycopg2
from psycopg2.extras import DictCursor
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from .database_sqlalchemy import Base

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


class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
