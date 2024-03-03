from fastapi import FastAPI

from controller.crud import CRUD
from databases import database_sqlalchemy, model

model.Base.metadata.create_all(bind=database_sqlalchemy.engine)
app = FastAPI()
app.include_router(CRUD)
