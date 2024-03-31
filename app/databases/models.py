# SQLAlchemy models to interact with db.
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .database_sqlalchemy import Base

# import psycopg2
# from psycopg2.extras import DictCursor
# import time
# while True:
#     try:
#         # Connect to your postgres DB
#         postgres_connection = psycopg2.connect(
#             database="fastapi",
#             user="postgres",
#             password="passwd",
#             cursor_factory=DictCursor,
#         )

#         # Open a cursor to perform database operations
#         postgres_cursor = postgres_connection.cursor()
#         print("Postgress connected")
#         break

#     except Exception as error:
#         print("Postgres connection failed")
#         print("Error: ", error)
#         time.sleep(2)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship(User)


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )
