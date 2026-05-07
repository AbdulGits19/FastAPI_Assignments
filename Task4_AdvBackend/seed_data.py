from Backend.app.database import SessionLocal, engine, Base
from Backend.app import models

Base.metadata.create_all(bind=engine)

db = SessionLocal()
doctors = [
    {"name": f"Dr. {name}", "specialization": spec, "email": f"{name}@hosp.com"}
    for name, spec in [
        ("Smith", "Cardiology"), ("Jones", "Neurology"), ("Brown", "Cardiology"),
        ("Wilson", "Dermatology"), ("Taylor", "Neurology"), ("Anderson", "Pediatrics"),
        ("Thomas", "Cardiology"), ("Jackson", "Dermatology"), ("White", "Pediatrics"),
        ("Harris", "Neurology"), ("Martin", "General"), ("Lee", "General")
    ]
]

for doc in doctors:
    if not db.query(models.Doctor).filter(models.Doctor.email == doc['email']).first():
        db.add(models.Doctor(**doc))

db.commit()
print("✅ 12 Doctors seeded!")