import oauth2 as oauth2
from databases import database_sqlalchemy, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

vote_router = APIRouter(tags=["Vote"], prefix="/vote")


@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database_sqlalchemy.get_db),
    current_user: schemas.TokenPayload = Depends(oauth2.get_current_user),
):
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist.",
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already voted"
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist."
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return f"Successfully deleted vote."
