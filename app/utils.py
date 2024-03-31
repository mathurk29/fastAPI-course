import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(passowrd: str):
    return pwd_context.hash(passowrd)


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
