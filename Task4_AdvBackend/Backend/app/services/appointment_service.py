from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException
from datetime import timedelta

# --- TASK 4 REQUIREMENT: Service Layer Architecture ---

def create_appointment(db: Session, app_data: schemas.AppointmentCreate):
    """
    Handles booking with double-booking prevention and slot validation.
    """
    # 1. REQUIREMENT: Validate Time Slots (Example: Only 9 AM to 5 PM)
    if not (9 <= app_data.appointment_date.hour <= 17):
        raise HTTPException(
            status_code=400, 
            detail="Appointments can only be scheduled between 09:00 and 17:00."
        )

    # 2. REQUIREMENT: Prevent Double Booking
    # We check if this doctor has any 'Pending' or 'Approved' appointment 
    # within 30 minutes of the requested time.
    buffer_start = app_data.appointment_date - timedelta(minutes=29)
    buffer_end = app_data.appointment_date + timedelta(minutes=29)

    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == app_data.doctor_id,
        models.Appointment.status.in_(["Pending", "Approved"]),
        models.Appointment.appointment_date.between(buffer_start, buffer_end)
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400, 
            detail="This doctor is already booked for a nearby time slot."
        )

    # 3. Create the record if all checks pass
    new_app = models.Appointment(
        doctor_id=app_data.doctor_id,
        patient_id=app_data.patient_id,
        appointment_date=app_data.appointment_date,
        status="Pending" # Default status for Task 4 workflow
    )
    
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def update_appointment_status(db: Session, appointment_id: int, new_status: str):
    """
    REQUIREMENT: Status handling (Approved, Rejected, Completed)
    """
    db_app = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_app:
        return None
        
    db_app.status = new_status
    db.commit()
    db.refresh(db_app)
    return db_app