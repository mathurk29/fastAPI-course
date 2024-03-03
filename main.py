from fastapi import FastAPI
from controller.routes import router
from databases import database_sqlalchemy
from databases import model, database_sqlalchemy

model.Base.metadata.create_all(bind=database_sqlalchemy.engine)


app = FastAPI()


# Dependency
def get_db():
    db = database_sqlalchemy.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(router)
