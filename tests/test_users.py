from app.databases import schemas

from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.json() == "Hello World"


def test_create_user(client):
    # explicily specify trailing slash otherwise the status_code would be 307 Redirect.
    # using json as endpoint accpets json body.
    res = client.post("/users/", json={"email": "ksh2@gmail.com", "password": "123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "ksh2@gmail.com"
    assert res.status_code == 201


def test_login_user(client):
    # using data as endpoint accepts form data.
    res = client.post("/login", data={"username": "ksh2@gmail.com", "password": "123"})
    assert res.status_code == 200
