from fastapi import FastAPI, HTTPException, status

# from database_es import wsl_elasticsearch
from database_dict import database, idx
from database_postgress import cur, conn
from model import Post
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"OK"}


@router.get("/posts")
def get_posts():
    cur.execute(""" SELECT * FROM posts""")
    posts = cur.fetchall()
    return posts


@router.get("/posts/{id}")
def get_posts_id(id: int):

    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} is not available ",
        )
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
        (post.title, post.content, post.published),
    )
    idx = cur.fetchone()[0]
    conn.commit()
    return f"Your post is successfully registered at index: {idx}"


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),))
    deleted_post_id = cur.fetchone()[0]
    conn.commit()
    if deleted_post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found.",
        )
    return f"Post at {deleted_post_id} removed successfully."


@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    cur.execute(
        """ UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING id""",
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ),
    )
    updated_post_id = cur.fetchone()
    conn.commit()
    if updated_post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not avaialbe.",
        )
    return f"Updated post with id: {id}"
