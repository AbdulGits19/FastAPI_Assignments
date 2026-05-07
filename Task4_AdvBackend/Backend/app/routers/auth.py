# Backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from Backend.app import schemas, database
from Backend.app.services import auth_service 
from .. import core_auth

router = APIRouter()

@router.post("/register", response_model=schemas.StandardResponse[schemas.UserResponse])
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Uses the service layer to handle the DB work
    new_user = auth_service.register_user(db, user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )
    
    return schemas.StandardResponse(
        message="User registered successfully",
        data=new_user
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Change this
    db: Session = Depends(database.get_db)
):
    from Backend.app.services import auth_service
    # Use form_data.username instead of user_data.username
    user = auth_service.get_user_by_username(db, form_data.username)
    
    if not user or not core_auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {
        "access_token": core_auth.create_access_token({"sub": user.username}), 
        "token_type": "bearer"
    }

@router.post("/forgot-password")
async def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    """REQUIREMENT: Forgot password functionality + Background Tasks"""
    from Backend.app.services import auth_service
    # Simulate finding user and generating a token
    token = auth_service.generate_reset_token(db, email) 
    
    # Simulate sending email in background
    background_tasks.add_task(print, f"EMAIL SENT: Reset your password using token: {token}")
    
    return {"message": "If the email exists, a reset link has been sent."}

@router.post("/reset-password")
def reset_password(username: str, new_password: str, db: Session = Depends(database.get_db)):
    """REQUIREMENT: Reset password functionality"""
    from Backend.app.services import auth_service
    success = auth_service.reset_password(db, username, new_password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password has been updated successfully"}