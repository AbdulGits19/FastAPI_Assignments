# Backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Generic, TypeVar, Any

# Placeholder for any data type (Generic)
T = TypeVar("T")

# --- API Response Standardization ---
class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "Operation successful"
    data: Optional[T] = None
    error: Optional[Any] = None
    
    # Modern Pydantic V2 config
    model_config = ConfigDict(from_attributes=True)

# --- Pagination Wrapper ---
class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    data: List[T] # Make sure this is List[T] from typing
    
    model_config = ConfigDict(from_attributes=True)

# --- AUTH SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "Patient" 

class UserResponse(BaseModel):
    id: int
    username: str
    role: str 
    model_config = ConfigDict(from_attributes=True)

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

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# --- PATIENT SCHEMAS ---
class PatientBase(BaseModel):
    name: str
    age: int = Field(..., ge=0)
    gender: str
    phone: str
    
class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- APPOINTMENT SCHEMAS ---
class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    status: str

class AppointmentResponse(AppointmentBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)

# --- REPORT SCHEMAS ---
class ReportBase(BaseModel):
    patient_id: int
    filename: str

class ReportResponse(ReportBase):
    id: int
    upload_date: datetime
    model_config = ConfigDict(from_attributes=True)