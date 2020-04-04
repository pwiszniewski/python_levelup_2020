from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message': 'Hello Hello World during the coronavirus pandemic!'}