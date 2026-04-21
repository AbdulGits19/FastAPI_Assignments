from pydantic import BaseModel, EmailStr, Field

class Doctor(BaseModel):
    name: str
    specialization: str
    email: EmailStr # special data type that follows standard email format
    is_active: bool = True

class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, description="Age must be greater than zero") # this enforces age that is > 0
    phone: str