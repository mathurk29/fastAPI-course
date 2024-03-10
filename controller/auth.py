from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import utils
from databases import models, schemas
from databases.database_sqlalchemy import get_db
from oauth2 import create_access_token

login_router = APIRouter(tags=["Authentication"])


@login_router.get("/login")
def login(user_credential: schemas.UserCreate, db: Session = Depends(get_db)):
    user = (
        db.query(models.User).filter(models.User.email == user_credential.email).first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if utils.verify_password_hash(user_credential.password, user.password):
        access_token = create_access_token(payload={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect credentials"
        )
