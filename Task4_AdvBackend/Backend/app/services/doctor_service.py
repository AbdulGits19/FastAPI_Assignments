from sqlalchemy.orm import Session
from .. import models

# --- TASK 4 REQUIREMENT: Service Layer Architecture ---

def get_doctors(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    name: str = None, 
    specialization: str = None,
    sort_by: str = "name"
):
    """
    REQUIREMENT: Advanced Search, Filtering, Pagination & Sorting
    """
    query = db.query(models.Doctor)

    # 1. Search & Filtering logic
    if name:
        # Performs a 'case-insensitive' search for the name
        query = query.filter(models.Doctor.name.contains(name))
    
    if specialization:
        query = query.filter(models.Doctor.specialization == specialization)

    # 2. Sorting logic
    if sort_by == "name":
        query = query.order_by(models.Doctor.name.asc())
    elif sort_by == "specialization":
        query = query.order_by(models.Doctor.specialization.asc())

    # 3. Pagination logic (limit and offset)
    total = query.count()
    # .offset skips a number of records, .limit stops after a certain amount
    data = query.offset(skip).limit(limit).all()

    return {"total": total, "data": data}

def create_doctor(db: Session, doctor_data):
    """
    Business logic for adding a new doctor to the system.
    """
    new_doc = models.Doctor(**doctor_data.model_dump())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc