from fastapi import FastAPI

from controller.crud import crud_router
from controller.user import user_router
from databases import database_sqlalchemy, models

models.Base.metadata.create_all(bind=database_sqlalchemy.engine)
app = FastAPI()
app.include_router(crud_router)
app.include_router(user_router)
