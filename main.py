from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    surename: str

class PatientWithID(BaseModel):
    id: int
    patient: Patient

app = FastAPI()
app.counter = 0
app.patients = []

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

@app.post('/patient', response_model=PatientWithID)
def patient_post(patient: Patient):
    app.patients.append(patient)
    app.counter += 1
    return PatientWithID(id=app.counter, patient=patient)
    # return {"id": app.counter, "patient": patient}
    # return {"id": app.counter, "patient": {"name": f'{patient.name}', "surename": f'{patient.surename}'}}

@app.get('/patient/{id}')
def patient_get(id):
    id = int(id)
    if id < 1 or id > app.counter:
        raise HTTPException(status_code=404, detail="Item not found")
    return app.patients[id-1]
