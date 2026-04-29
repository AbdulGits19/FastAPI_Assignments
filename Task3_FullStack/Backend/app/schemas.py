from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# --- AUTH SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- DOCTOR SCHEMAS ---
class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: EmailStr

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

# --- PATIENT SCHEMAS ---
class PatientBase(BaseModel):
    name: str
    age: int = Field(..., ge=0)  # Changed from gt=0 to ge=0
    gender: str
    phone: str

    
class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    class Config:
        from_attributes = True

# --- APPOINTMENT SCHEMAS ---
class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    # Change doctor_id and patient_id to Optional just in case
    doctor_id: Optional[int] = None 
    patient_id: Optional[int] = None
    status: str = "Scheduled"

    class Config:
        from_attributes = True

# --- REPORT SCHEMAS ---
class ReportBase(BaseModel):
    patient_id: int
    filename: str

class ReportResponse(ReportBase):
    id: int
    upload_date: datetime
    class Config:
        from_attributes = True




# ... keep your existing imports ...

# ADD THIS: For the /register response
class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

# ADD THIS: For the PUT /doctors/{id} route
class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = None

# ADD THIS: For the PUT /patients/{id} route
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None




