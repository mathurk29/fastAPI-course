from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.databases import database_sqlalchemy, models, schemas
from app.databases.database_sqlalchemy import get_db
from app.main import app

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = f"{settings.database_type}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DATABASE_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
)

models.Base.metadata.create_all(bind=engine)


# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_root():
    res = client.get("/")
    assert res.json() == "Hello World"


def test_create_user():
    res = client.post("/users/", json={"email": "ksh2@gmail.com", "password": "123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "ksh2@gmail.com"
    assert res.status_code == 201
