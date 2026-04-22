from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import jwt, JWTError

# DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


#Authentication

def get_current_active_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# --- GENERAL ROUTES ---
@app.get("/")
def home():
    return {"message": "The Hospital API is Live!"}

# --- DOCTOR ROUTES ---
@app.post("/doctors", response_model=schemas.DoctorResponse)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
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

# --- PATIENT ROUTES ---

@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user) 
):
    # This captures everything correctly from your PatientCreate schema
    new_patient = models.Patient(
        name=patient.name, 
        age=patient.age, 
        gender=patient.gender, 
        phone=patient.phone
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@app.get("/patients", response_model=list[schemas.PatientResponse])
def get_patients(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
    return db.query(models.Patient).all()

# --- APPOINTMENT ROUTES ---
@app.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
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
def get_all_appointments(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
    return db.query(models.Appointment).all()

# --- SEARCH & FILTERS ---
@app.get("/doctors/search/", response_model=list[schemas.DoctorResponse])
def search_doctors(specialization: str, db: Session = Depends(database.get_db)):
    return db.query(models.Doctor).filter(models.Doctor.specialization.contains(specialization)).all()

@app.get("/patients/search/", response_model=list[schemas.PatientResponse])
def search_patients(query: str, db: Session = Depends(database.get_db)):
    return db.query(models.Patient).filter(
        (models.Patient.name.contains(query)) | (models.Patient.phone.contains(query))
    ).all()

# --- USER AUTH ROUTES ---
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}