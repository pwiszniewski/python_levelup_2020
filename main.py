import secrets
from hashlib import sha256

from fastapi import Depends, FastAPI, HTTPException, status, Cookie, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

app = FastAPI()
app.secret_key = "99d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8aa34"
app.sessions = {}

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}

def get_session_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    if session_token not in app.sessions:
        app.sessions[session_token] = credentials.username
    return session_token


@app.post("/login")
def login_user(session_token: str = Depends(get_session_token)):
    response = RedirectResponse(url='/welcome')
    response.set_cookie(key="session_token", value=session_token)
    return response

@app.post("/logout")
def logout_user(*, response: Response, session_token: str = Cookie(None)):
    print(app.sessions)
    print(session_token)
    if session_token not in app.sessions:
        raise HTTPException(status_code=403, detail="Unauthorised")
    app.sessions.remove(session_token)
    return RedirectResponse(url='/')

@app.get('/welcome')
def welcome(*, request: Request, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(status_code=403, detail="Unathorised")
    return templates.TemplateResponse("welcome.html", {"request": request, "user": app.sessions[session_token]})