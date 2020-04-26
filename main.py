import secrets
from hashlib import sha256

from fastapi import Depends, FastAPI, HTTPException, status, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI()
app.secret_key = "99d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8aa34"

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


@app.post("/login")
def read_current_user(username: str = Depends(get_current_username)):
    session_token = sha256(bytes(f"{user}{password}{app.secret_key}")).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    return RedirectResponse(url='/welcome')
    