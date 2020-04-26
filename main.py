from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}

@app.get('/welcome')
def method_get():
    return {'message': 'Welcome!'}
