from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
def root():
    return {'OK'}


@app.get('/posts')
def get_posts():
    return {'data': "This is your posts"}


@app.post('/posts')
def create_posts(post: Post):
    return {"data": post.dict()}
