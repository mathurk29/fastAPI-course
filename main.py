from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

id = 1
database = dict()


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
    return database


@app.get('/posts/{id}')
def get_posts_id(id: int):
    print('here')
    try:
        result = database[id]
        return result
    except KeyError:
        return f"Key not found in: {database}"


@app.post('/posts')
def create_posts(post: Post):
    global id
    database[id] = post.dict()
    id = id + 1
    return database
