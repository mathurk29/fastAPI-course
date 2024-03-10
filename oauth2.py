from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

# SECRET_KEY
# Algorith
# Expiration

# to get a string like this run:
# openssl rand -hex 32
SECRTE_KEY = "71d9c2db8acb64e6a7e0cb6bfff07c4e2f10a819108fa1ad49bb0862c2a42fcf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRTE_KEY, algorithm=ALGORITHM)
    return encoded_jwt
