from datetime import datetime

from pydantic import BaseModel


class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Posts(PostsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
