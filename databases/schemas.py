from pydantic import BaseModel


class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostsCreate(PostsBase):
    pass
