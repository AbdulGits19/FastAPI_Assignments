from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from Backend.app import models, database, schemas
from Backend.app.utils.file_handler import validate_file

router = APIRouter()

# Fixed: Now supports both URL styles
@router.post("/{patient_id}/upload")
async def upload(patient_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # REQUIREMENT: Enhanced File Handling (Size/Type check)
    validate_file(file)
    new_report = models.Report(patient_id=patient_id, filename=file.filename)
    db.add(new_report)
    db.commit()
    return {"message": "File uploaded"}

# Fixed: Removed the wrong decorator from here
@router.get("/", response_model=schemas.PaginatedResponse[schemas.PatientResponse])
def list_patients(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 10):
    safe_limit = limit if limit > 0 else 10
    query = db.query(models.Patient)
    total = query.count()
    patients = query.offset(skip).limit(safe_limit).all()
    
    return {
        "total": total,
        "page": (skip // safe_limit) + 1,
        "limit": safe_limit,
        "data": patients
    }

# This is where /{patient_id}/files actually belongs
@router.get("/{patient_id}/files")
def list_files(patient_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Report).filter(models.Report.patient_id == patient_id).all()

@router.get("/{patient_id}/files/{file_id}/download")
def download(file_id: int):
    return {"message": "Downloading file..."}

@router.delete("/{patient_id}/files/{file_id}/delete")
def delete_file(file_id: int, db: Session = Depends(database.get_db)):
    db.query(models.Report).filter(models.Report.id == file_id).delete()
    db.commit()
    return {"message": "File deleted"}