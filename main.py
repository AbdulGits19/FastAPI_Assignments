from fastapi import FastAPI, HTTPException
from uuid import uuid4
from models import Doctor, Patient 
from database import doctors, patients 

app = FastAPI() #

@app.get('/')
def home():
    return {'message': 'API is working !!!!!!'}

# Doctor APIs

@app.post('/doctors')
def create_doctor(doctor: Doctor):
    doctor_data = doctor.model_dump() # this model.dump Converts obj into dictionary
    doctor_data['id'] = str(uuid4()) # this gives each doctor a unique id
    doctors.append(doctor_data)
    return doctor_data

@app.get('/doctors')
def get_all_doctors():
    return doctors # here, we are returning the full doctors list

@app.get('/doctors/{doctor_id}')
def get_doctor(doctor_id: str):
    for doc in doctors:
        if doc['id'] == doctor_id: #checking if any doctor matches with the input id
            return doc
    raise HTTPException(status_code=404, detail='No Such Doctor Found')

#  Patient APIs 

@app.post('/patients')
def create_patient(patient: Patient):
    patient_data = patient.model_dump() # same as doctors, turing into dictionaries
    patient_data['id'] = str(uuid4()) # unique patient id
    patients.append(patient_data)
    return patient_data 

@app.get('/patients')
def get_all_patients():
    return patients # here, we are returning the full patients list