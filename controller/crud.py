from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from databases import model
from databases.database_sqlalchemy import get_db

CRUD = APIRouter()


@CRUD.get("/")
def root():
    return {"OK"}


@CRUD.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # postgres_cursor.execute(""" SELECT * FROM posts""")
    # posts = postgres_cursor.fetchall()
    posts = db.query(model.Post)
    return posts


@CRUD.get("/posts/{id}")
def get_posts_id(id: int):

    model.postgres_cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = model.postgres_cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} is not available ",
        )
    return post


@CRUD.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: model.PostsBase):
    model.postgres_cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
        (post.title, post.content, post.published),
    )
    idx = model.postgres_cursor.fetchone()[0]
    model.postgres_connection.commit()
    return f"Your post is successfully registered at index: {idx}"


@CRUD.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    model.postgres_cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),)
    )
    temp = model.postgres_cursor.fetchone()
    if temp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found.",
        )
    deleted_post_id = temp[0]
    model.postgres_connection.commit()


@CRUD.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: model.PostsBase):
    model.postgres_cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING id""",
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ),
    )
    updated_post_id = model.postgres_cursor.fetchone()
    model.postgres_connection.commit()
    if updated_post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not avaialbe.",
        )
    return f"Updated post with id: {id}"


@CRUD.get("/sqlalchemy_test")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Posts).all()
    return posts
