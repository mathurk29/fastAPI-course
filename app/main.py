from controller.auth import login_router
from controller.crud import crud_router
from controller.user import user_router
from controller.vote import vote_router
from databases import database_sqlalchemy, models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=database_sqlalchemy.engine)

app = FastAPI()

origins = ["https://www.localhost.com/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud_router)
app.include_router(user_router)
app.include_router(login_router)
app.include_router(vote_router)


@app.get("/")
def root():
    return "Hello World"
