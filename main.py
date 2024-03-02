from fastapi import FastAPI
from routes import router
import database_postgress
import database_es

app = FastAPI()
app.include_router(router)
