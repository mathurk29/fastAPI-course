import imp
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import settings
from databases import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# Algorith
# Expiration

# to get a string like this run:
# openssl rand -hex 32
SECRTE_KEY = settings.SECRTE_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRTE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        paylaod = jwt.decode(token, SECRTE_KEY, algorithms=[ALGORITHM])
        id: int = paylaod.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenPayload(id=id)
        return token_data
    except JWTError:
        raise credentials_exceptions


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )
    return verify_access_token(token, credentials_exceptions)
