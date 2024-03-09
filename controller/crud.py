from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from databases import models, schemas
from databases.database_sqlalchemy import get_db

crud_router = APIRouter(prefix="/posts", tags=["posts"])


@crud_router.get("/", response_model=List[schemas.Posts])
def get_posts(db: Session = Depends(get_db)):
    # postgres_cursor.execute(""" SELECT * FROM posts""")
    # posts = postgres_cursor.fetchall()
    posts = db.query(models.Posts).all()
    return posts


@crud_router.get("/{id}", response_model=schemas.Posts)
def get_posts_id(id: int, db: Session = Depends(get_db)):

    # model.postgres_cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = model.postgres_cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} is not available ",
        )
    return post


@crud_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Posts
)
def create_posts(post: schemas.PostsBase, db: Session = Depends(get_db)):
    # model.postgres_cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
    #     (post.title, post.content, post.published),
    # )
    # idx = model.postgres_cursor.fetchone()[0]
    # model.postgres_connection.commit()
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@crud_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    # model.postgres_cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),)
    # )
    # temp = model.postgres_cursor.fetchone()
    posts = db.query(models.Posts).filter(models.Posts.id == id)
    if posts.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found.",
        )
    posts.delete(synchronize_session=False)
    db.commit()


@crud_router.put(
    "/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Posts
)
def update_post(id: int, post: schemas.PostsBase, db: Session = Depends(get_db)):
    # model.postgres_cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING id""",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         str(id),
    #     ),
    # )
    # updated_post_id = model.postgres_cursor.fetchone()
    # model.postgres_connection.commit()
    update_query = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = update_query.first()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not avaialbe.",
        )
    update_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return updated_post
