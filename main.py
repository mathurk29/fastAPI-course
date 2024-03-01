from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
def root():
    return {'OK'}

@app.post('/createposts')
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {'message': f"successfully created posts : {payload['key']}"}