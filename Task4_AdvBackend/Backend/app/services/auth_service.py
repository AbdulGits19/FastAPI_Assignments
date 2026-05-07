from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import security
from Backend.app import core_auth

# --- TASK 4 REQUIREMENT: Service Layer Architecture ---

def register_user(db: Session, user_data: schemas.UserCreate):
    """
    Handles user registration with password hashing.
    """
    # 1. Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        return None # The router will handle the 400 error
    
    # 2. TASK 4 REQUIREMENT: Password hashing (bcrypt)
    hashed_pass = security.get_password_hash(user_data.password)
    
    # 3. Create the user with the role from our new schema
    new_user = models.User(
        username=user_data.username,
        hashed_password=hashed_pass,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    """
    Helper to find a user for the login process.
    """
    return db.query(models.User).filter(models.User.username == username).first()


import uuid

def generate_reset_token(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    # In a real app, you'd save this token to the DB with an expiry
    # For Task 4, we simulate generating a unique reset link
    reset_token = str(uuid.uuid4())
    return reset_token

def reset_password(db: Session, username: str, new_password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    user.hashed_password = core_auth.get_password_hash(new_password)
    db.commit()
    return True