from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Optional
from sqlalchemy.orm import Session
from Backend.app import models, schemas, database
from Backend.app.services import appointment_service
from Backend.app.utils.deps import is_doctor_or_admin

router = APIRouter()

@router.post("/", response_model=schemas.StandardResponse[schemas.AppointmentResponse])
def book_appointment(
    app_data: schemas.AppointmentCreate, 
    db: Session = Depends(database.get_db)
):
    """
    REQUIREMENT: Enhanced Appointment Handling
    Logic: Service layer checks for double-booking.
    """
    # The service will raise a 400 error if there's a conflict
    new_app = appointment_service.create_appointment(db, app_data)
    
    return schemas.StandardResponse(
        data=new_app, 
        message="Appointment successfully booked."
    )

def create_appointment(db: Session, app_data: schemas.AppointmentCreate):
    # 1. REQUIREMENT: Conflict Handling (Double-Booking Prevention)
    # Check if the doctor is already booked at this exact time
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == app_data.doctor_id,
        models.Appointment.appointment_date == app_data.appointment_date
    ).first()

    if existing_appointment:
        # If we find a match, raise an error immediately
        raise HTTPException(
            status_code=400, 
            detail="Conflict: This doctor is already booked for this time slot."
        )

    # 2. Check if the patient is already booked at this exact time (Optional but good)
    existing_patient_app = db.query(models.Appointment).filter(
        models.Appointment.patient_id == app_data.patient_id,
        models.Appointment.appointment_date == app_data.appointment_date
    ).first()

    if existing_patient_app:
        raise HTTPException(
            status_code=400, 
            detail="Conflict: This patient already has another appointment at this time."
        )

    # 3. If no conflicts, save the record
    new_app = models.Appointment(**app_data.model_dump(), status="Scheduled")
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.put("/{app_id}/status", response_model=schemas.StandardResponse[schemas.AppointmentResponse], dependencies=[Depends(is_doctor_or_admin)])
def update_status(
    app_id: int, 
    update: schemas.AppointmentUpdate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(database.get_db)
):
    """
    REQUIREMENT: Appointment Status Workflow + Background Tasks
    """
    updated_app = appointment_service.update_appointment_status(db, app_id, update.status)
    if not updated_app:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # REQUIREMENT: Background Task (Simulating an automated email)
    if update.status in ["Approved", "Cancelled"]:
        background_tasks.add_task(
            print, f"SYSTEM NOTIFICATION: Appointment {app_id} status changed to {update.status}"
        )
        
    return schemas.StandardResponse(
        data=updated_app, 
        message=f"Appointment status has been updated to {update.status}"
    )

@router.get("/", response_model=schemas.PaginatedResponse[schemas.AppointmentResponse])
def list_appointments(
    status: Optional[str] = None,
    patient_id: Optional[int] = None,
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    REQUIREMENT: Advanced Search/Filter + Pagination
    """
    safe_limit = limit if limit > 0 else 10
    
    query = db.query(models.Appointment)
    if status:
        query = query.filter(models.Appointment.status == status)
    if patient_id:
        query = query.filter(models.Appointment.patient_id == patient_id)
    
    total = query.count()
    data = query.offset(skip).limit(safe_limit).all()
    
    return schemas.PaginatedResponse(
        total=total, 
        page=(skip // safe_limit) + 1, 
        limit=safe_limit, 
        data=data
    )