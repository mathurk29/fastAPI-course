from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import utils
from databases import models, schemas
from databases.database_sqlalchemy import get_db

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.create_password_hash(user.password)
    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return new_user


@user_router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
