# Pydantic schemas for Request-Response Validation.

from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Posts(PostsBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class ConfigDict:
        from_attributes = True


class PostsOut(BaseModel):
    Posts: Posts
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
