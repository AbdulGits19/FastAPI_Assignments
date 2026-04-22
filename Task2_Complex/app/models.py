from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .database import Base # This Base is defined from the database.py

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    age = Column(Integer)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id")) # Link to Doctor
    patient_id = Column(Integer, ForeignKey("patients.id")) # Link to Patient
    appointment_date = Column(DateTime)
    status = Column(String, default="Scheduled") # Scheduled, Completed, Cancelled



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # Never store plain text!