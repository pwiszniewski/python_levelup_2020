from fastapi import FastAPI

from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    surename: str

app = FastAPI()
app.counter = 0

@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}

@app.get('/method')
def method_get():
    return {'method': 'GET'}

@app.post('/method')
def method_post():
    return {'method': 'POST'}

@app.put('/method')
def method_put():
    return {'method': 'PUT'}

@app.delete('/method')
def method_delete():
    return {'method': 'DELETE'}

@app.post('/patient')
def patient_post(patient: Patient):
    app.counter += 1
    return {"id": app.counter, "patient": {"name": f'{patient.name}', "surename": f'{patient.surename}'}}


