from fastapi import APIRouter, HTTPException, status

# from database_es import wsl_elasticsearch
from databases.model import PostsBase, postgres_connection, postgres_cursor

router = APIRouter()


@router.get("/")
def root():
    return {"OK"}


@router.get("/posts")
def get_posts():
    postgres_cursor.execute(""" SELECT * FROM posts""")
    posts = postgres_cursor.fetchall()
    return posts


@router.get("/posts/{id}")
def get_posts_id(id: int):

    postgres_cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = postgres_cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} is not available ",
        )
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostsBase):
    postgres_cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id""",
        (post.title, post.content, post.published),
    )
    idx = postgres_cursor.fetchone()[0]
    postgres_connection.commit()
    return f"Your post is successfully registered at index: {idx}"


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    postgres_cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),)
    )
    temp = postgres_cursor.fetchone()
    if temp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found.",
        )
    deleted_post_id = temp[0]
    postgres_connection.commit()


@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: PostsBase):
    postgres_cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING id""",
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ),
    )
    updated_post_id = postgres_cursor.fetchone()
    postgres_connection.commit()
    if updated_post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not avaialbe.",
        )
    return f"Updated post with id: {id}"
