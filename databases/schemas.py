# Pydantic schemas for Request-Response Validation.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Posts(PostsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: Optional[int] = None
