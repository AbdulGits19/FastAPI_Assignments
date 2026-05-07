from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from Backend.app import schemas, database, models
from Backend.app.services import doctor_service
from Backend.app.utils.deps import is_admin


router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse[schemas.DoctorResponse])
def list_doctors(
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    specialization: Optional[str] = None
):
    # 1. Prevent Division by Zero
    safe_limit = limit if limit > 0 else 10
    
    # 2. Start the query
    query = db.query(models.Doctor)
    
    # 3. RE-ADD SEARCH & FILTER LOGIC
    if name:
        query = query.filter(models.Doctor.name.contains(name))
    if specialization:
        query = query.filter(models.Doctor.specialization == specialization)
    
    # 4. Get total count for pagination metadata
    total = query.count()
    
    # 5. Apply pagination
    doctors = query.offset(skip).limit(safe_limit).all()
    
    # 6. RETURN THE CORRECT STRUCTURE
    return schemas.PaginatedResponse(
        total=total,
        page=(skip // safe_limit) + 1,
        limit=safe_limit,
        data=doctors
    )

@router.post("/", dependencies=[Depends(is_admin)]) # REQUIREMENT: RBAC (Admin Only)
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db)):
    return doctor_service.create_doctor(db, doctor)


@router.get("/{doc_id}", response_model=schemas.StandardResponse[schemas.DoctorResponse])
def get_doctor(doc_id: int, db: Session = Depends(database.get_db)):
    doc = db.query(models.Doctor).filter(models.Doctor.id == doc_id).first()
    if not doc: raise HTTPException(status_code=404, detail="Doctor not found")
    return schemas.StandardResponse(data=doc)

@router.put("/{doc_id}", dependencies=[Depends(is_admin)])
def update_doctor(doc_id: int, obj: schemas.DoctorUpdate, db: Session = Depends(database.get_db)):
    db_obj = db.query(models.Doctor).filter(models.Doctor.id == doc_id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in obj.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    return schemas.StandardResponse(message="Doctor updated")

@router.delete("/{doc_id}", dependencies=[Depends(is_admin)])
def delete_doctor(doc_id: int, db: Session = Depends(database.get_db)):
    db.query(models.Doctor).filter(models.Doctor.id == doc_id).delete()
    db.commit()
    return schemas.StandardResponse(message="Doctor deleted")