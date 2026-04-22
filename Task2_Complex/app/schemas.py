from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# Doctor Schemas

class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: EmailStr

class DoctorCreate(DoctorBase):
    pass # Used when creating a doctor (Postman -> API)

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True # This allows Pydantic to read SQLAlchemy models

# Patient Schemas 

class PatientBase(BaseModel):
    name: str
    phone: str
    age: int = Field(gt=0, description='Age must be > 0')

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True

# Appointment Schemas

class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True


# User login schema

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str