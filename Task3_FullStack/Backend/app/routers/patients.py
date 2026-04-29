from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os, shutil
from .. import models, schemas, database, auth

router = APIRouter() # No global lock here, we will lock specific routes below
UPLOAD_DIR = "app/uploads"

# 1. GET ALL PATIENTS (Public or Locked - Your choice)
@router.get("/", response_model=List[schemas.PatientResponse])
def get_patients(db: Session = Depends(database.get_db)):
    return db.query(models.Patient).all()

# 2. CREATE PATIENT (Locked with the 'current_user' dependency)
@router.post("/", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user) # The Lock icon
):
    new_pat = models.Patient(**patient.model_dump())
    db.add(new_pat)
    db.commit()
    db.refresh(new_pat)
    return new_pat

# --- UPDATE PATIENT ---
@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int, 
    patient_update: schemas.PatientUpdate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_pat = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_pat:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update the fields
    for key, value in patient_update.model_dump(exclude_unset=True).items():
        setattr(db_pat, key, value)
    
    db.commit()
    db.refresh(db_pat)
    return db_pat

# --- DELETE PATIENT (New!) ---
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_pat = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
    if not db_pat:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Important: Check if this patient has active appointments before deleting
    # or the database might throw a Foreign Key error!
    db.delete(db_pat)
    db.commit()
    return {"message": f"Patient {patient_id} has been removed from the system."}

# --- PATIENT FILES SECTION ---

# 5. UPLOAD FILE (Locked)
@router.post("/{patient_id}/upload")
async def upload_file(
    patient_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user) # The Lock icon
):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, f"{patient_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_report = models.Report(patient_id=patient_id, filename=file.filename)
    db.add(new_report)
    db.commit()
    return {"message": "File uploaded successfully"}

# 5. GET FILES (Locked)
@router.get("/{patient_id}/files", response_model=List[schemas.ReportResponse])
def get_patient_files(
    patient_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user) # The Lock icon
):
    return db.query(models.Report).filter(models.Report.patient_id == patient_id).all()