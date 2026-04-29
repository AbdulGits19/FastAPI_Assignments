from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas, database, auth
from ..websocket import manager

router = APIRouter()

# 1. CREATE APPOINTMENT (With Validation)
@router.post("/", response_model=schemas.AppointmentResponse)
async def create_appointment(
    app_data: schemas.AppointmentCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Check if doctor and patient exist first
    doctor = db.query(models.Doctor).filter(models.Doctor.id == app_data.doctor_id).first()
    patient = db.query(models.Patient).filter(models.Patient.id == app_data.patient_id).first()
    
    if not doctor or not patient:
        raise HTTPException(status_code=404, detail="Doctor or Patient not found in database")

    # Create the record
    new_app = models.Appointment(**app_data.model_dump())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    # Trigger WebSocket with Names instead of just IDs
    await manager.broadcast(f"📢 Alert: {patient.name} just booked an appointment with Dr. {doctor.name}!")
    
    return new_app

# 2. GET ALL APPOINTMENTS (The "Not Working" Fix)
@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(db: Session = Depends(database.get_db)):
    # We use .all() but ensure the database isn't returning junk
    appointments = db.query(models.Appointment).all()
    
    # If this returns 422 in Swagger, check your schemas.AppointmentResponse 
    # and make sure every field (like status) has a default value.
    return appointments

# 3. CANCEL APPOINTMENT

@router.put("/{appointment_id}/cancel")
async def cancel_appointment(
    appointment_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user) # The Lock
):
    
    db_app = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db_app.status = "Cancelled"
    db.commit()
    
    await manager.broadcast(f"⚠️ Appointment {appointment_id} has been cancelled.")
    return {"message": "Appointment cancelled successfully"}