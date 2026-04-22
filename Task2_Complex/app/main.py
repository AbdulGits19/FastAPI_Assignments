from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import jwt, JWTError

# Add this one

# Create the DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- AUTHENTICATION UTILS ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# --- GENERAL ROUTES ---

@app.get("/")
def home():
    return {"message": "Hospital API is Live!"}

# --- DOCTOR ROUTES ---

@app.post("/doctors", response_model=schemas.DoctorResponse)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.email == doctor.email).first()
    if db_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_doctor = models.Doctor(name=doctor.name, specialization=doctor.specialization, email=doctor.email)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@app.get("/doctors", response_model=list[schemas.DoctorResponse])
def get_all_doctors(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 10):
    return db.query(models.Doctor).offset(skip).limit(limit).all()

@app.put("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int, doctor_update: schemas.DoctorUpdate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    update_data = doctor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doctor)
    db.commit()
    return {"message": f"Doctor with ID {doctor_id} has been deleted"}

# --- APPOINTMENT ROUTES ---

@app.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    # Check if doctor and patient exist
    doc = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
    pat = db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first()
    if not doc or not pat:
        raise HTTPException(status_code=404, detail="Doctor or Patient not found")

    new_app = models.Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@app.get("/appointments", response_model=list[schemas.AppointmentResponse])
def get_all_appointments(db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    return db.query(models.Appointment).all()

# --- SEARCH & FILTERS ---

@app.get("/doctors/search/", response_model=list[schemas.DoctorResponse])
def search_doctors(specialization: str, db: Session = Depends(database.get_db)):
    return db.query(models.Doctor).filter(models.Doctor.specialization.contains(specialization)).all()

@app.get("/patients/search/", response_model=list[schemas.PatientResponse])
def search_patients(query: str, db: Session = Depends(database.get_db)):
    # Added 'query: str' above so Python knows what this variable is
    return db.query(models.Patient).filter(
        (models.Patient.name.contains(query)) | (models.Patient.phone.contains(query))
    ).all()

@app.get("/appointments/doctor/{doc_id}", response_model=list[schemas.AppointmentResponse])
def get_doctor_appointments(doc_id: int, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doc_id).all()

# --- USER AUTH ROUTES ---

@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}