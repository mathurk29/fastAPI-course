from fastapi import FastAPI
from controller.routes import router
from databases import datadatabase_postgress
from databases import database_es

app = FastAPI()
app.include_router(router)
