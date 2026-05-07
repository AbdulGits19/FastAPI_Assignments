from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Backend.app.database import engine, Base 
from Backend.app.routers import auth, doctors, appointments, patients
from Backend.app import models
import logging
logging.basicConfig(
    filename='app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("HMS API Server started and logging initialized.")

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced Healthcare API")

# --- TASK 4 REQUIREMENT: Global Exception Handling ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # This catches ANY error and turns it into a Standardized JSON response
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred",
            "error": str(exc)
        }
    )

# # Include Routers (We'll update these in Step 10)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])



@app.get("/")
def root():
    return {"status": "success", "message": "API is online"}