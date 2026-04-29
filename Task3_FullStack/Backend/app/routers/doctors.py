from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, database, auth
from datetime import datetime, timedelta, timezone

router = APIRouter()

# 1. CREATE DOCTOR
@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(
    doctor: schemas.DoctorCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.email == doctor.email).first()
    if db_doctor:
        raise HTTPException(status_code=400, detail="Doctor with this email already exists")
    
    new_doc = models.Doctor(**doctor.model_dump())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# 2. GET ALL DOCTORS (Merged Search + Dynamic Availability)

@router.get("/", response_model=List[schemas.DoctorResponse])
def get_all_doctors(db: Session = Depends(database.get_db)):
    doctors = db.query(models.Doctor).all()
    now = datetime.now() 

    for doc in doctors:
        # Check for ANY appointment that is active right now
        # Status must not be cancelled
        active_app = db.query(models.Appointment).filter(
            models.Appointment.doctor_id == doc.id,
            models.Appointment.status != "Cancelled",
            models.Appointment.appointment_date <= now,
            models.Appointment.appointment_date >= now - timedelta(minutes=30)
        ).first()

        # OVERRIDE the status. 
        # If active_app exists, available = False. Else, True.
        doc.is_available = True if active_app is None else False
            
    return doctors


# 3. GET SYSTEM STATS (Place this here for logical grouping)
@router.get("/stats/summary")
def get_hospital_stats(db: Session = Depends(database.get_db)):
    total_patients = db.query(models.Patient).count()
    # Count only appointments that aren't cancelled
    active_appointments = db.query(models.Appointment).filter(
        models.Appointment.status != "Cancelled"
    ).count()
    
    return {
        "total_active_appointments": active_appointments,
        "total_patients": total_patients
    }

# 4. GET SINGLE DOCTOR
@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor_by_id(doctor_id: int, db: Session = Depends(database.get_db)):
    doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc

# 5. UPDATE DOCTOR
@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(
    doctor_id: int, 
    doctor_update: schemas.DoctorUpdate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in doctor_update.model_dump(exclude_unset=True).items():
        setattr(db_doc, key, value)
    
    db.commit()
    db.refresh(db_doc)
    return db_doc

# 6. DELETE DOCTOR
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doc)
    db.commit()
    return {"message": "Doctor deleted successfully"}