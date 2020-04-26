import secrets

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

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/login")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}