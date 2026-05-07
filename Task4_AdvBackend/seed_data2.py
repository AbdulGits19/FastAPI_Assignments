from Backend.app.database import SessionLocal, engine, Base
from Backend.app import models

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()
patients = [
    {"name": "Arthur Morgan", "age": 36, "gender": "Male", "phone": "555-0101"},
    {"name": "Sadie Adler", "age": 25, "gender": "Female", "phone": "555-0102"},
    {"name": "Krish Jain", "age": 30, "gender": "Male", "phone": "555-0103"},
     {"name": "John Yugandhar", "age": 30, "gender": "Male", "phone": "555-0103"},
      {"name": "Yuktha Mukundhan", "age": 30, "gender": "Female", "phone": "555-0103"}
]

for p in patients:
    if not db.query(models.Patient).filter(models.Patient.phone == p['phone']).first():
        db.add(models.Patient(**p))

db.commit()
print("✅ 3 Patients seeded!")