import logging
from . import websocket
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, websocket 
from .routers import auth, doctors, patients, appointments

# 1. Setup Logging (Requirement 6)
logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Doctor & Patient Management API")

# 3. CORS Middleware for React
# Add this block!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # This allows EVERY port (5173, 5174, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming: {request.method} {request.url}")
    response = await call_next(request)
    return response

# 5. Include All Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(websocket.router)
app.include_router(auth.router, prefix="/auth")

# IMPORTANT: Include the websocket router
app.include_router(websocket.router, tags=["Real-time Notifications"])

@app.get("/")
def home():
    return {"message": "Hospital System API is Live"}

@app.on_event("startup")
async def startup_event():
    print("✅ SERVER STARTING: WebSocket router is included.")

@app.get("/reset-doctors")
def reset_doctors(db: Session = Depends(database.get_db)):
    db.query(models.Doctor).update({models.Doctor.is_available: True})
    db.commit()
    return {"message": "All doctors set to Green!"}