from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()

security = HTTPBasic()

@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}

@app.get('/welcome')
def method_get():
    return {'message': 'Welcome!'}

@app.get("/login")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
