from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}

@app.get('/method')
def hello_world():
    return {'method': 'GET'}

@app.post('/method')
def hello_world():
    return {'method': 'POST'}

@app.put('/method')
def hello_world():
    return {'method': 'PUT'}

@app.delete('/method')
def hello_world():
    return {'method': 'DELETE'}