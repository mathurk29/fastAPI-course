from ast import mod
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import oauth2
from databases import models, schemas
from databases.database_sqlalchemy import get_db

crud_router = APIRouter(prefix="/posts", tags=["posts"])


@crud_router.get("/", response_model=List[schemas.PostsOut])
def get_posts(
    db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""
):
    # postgres_cursor.execute(""" SELECT * FROM posts""")
    # posts = postgres_cursor.fetchall()
    posts = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Posts.id == models.Vote.post_id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.content.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    posts = list(map(lambda x: x._mapping, posts))
    return posts


@crud_router.get("/{id}", response_model=schemas.PostsOut)
def get_posts_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    # model.postgres_cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = model.postgres_cursor.fetchone()
    post = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Posts.id == models.Vote.post_id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} is not available ",
        )
    return post


@crud_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Posts
)
def create_posts(
    post: schemas.PostsBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # model.postgres_cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
    #     (post.title, post.content, post.published),
    # )
    # idx = model.postgres_cursor.fetchone()[0]
    # model.postgres_connection.commit()
    new_post = models.Posts(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@crud_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # model.postgres_cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),)
    # )
    # temp = model.postgres_cursor.fetchone()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found.",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    post_query.delete(synchronize_session=False)
    db.commit()


@crud_router.put(
    "/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Posts
)
def update_post(
    id: int,
    post: schemas.PostsBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    update_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return updated_post
