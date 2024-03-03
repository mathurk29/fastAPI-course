from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_type = "postgresql"
db_username = "postgres"
db_password = "passwd"
db_IP_address = "localhost"
database_name = "fastapi"
SQLALCHEMY_DATABASE_URL = (
    f"{database_type}://{db_username}:{db_password}@{db_IP_address}/{database_name}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
