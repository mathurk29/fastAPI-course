from fastapi import FastAPI, HTTPException, status

# from database_es import wsl_elasticsearch
from database_dict import database, idx
from model import Post
from fastapi import APIRouter

router = APIRouter()


@ router.get('/')
def root():
    return {'OK'}


@ router.get('/posts')
def get_posts():
    return database


@ router.get('/posts/{id}')
def get_posts_id(id: int):
    print('here')
    if id not in database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Key {id} not found in: {database}")
    return database[id]


@ router.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    global idx
    database[idx] = post.dict()
    idx = idx + 1
    return f'Your post is registered at index: {idx}'


@ router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    if id not in database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Key {id} not found in: {database}")
    database.pop(id)


@ router.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    if id not in database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='id not available in database.')
    database[id].update(post.dict())
    return database[id]
