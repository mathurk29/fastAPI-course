from typing import Optional

from fastapi import FastAPI, HTTPException, status
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
    if id not in database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Key {id} not found in: {database}")
    return database[id]


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    global id
    database[id] = post.dict()
    id = id + 1
    return database


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    if id not in database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Key {id} not found in: {database}")
    database.pop(id)
