from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Backend.app.database import get_db

SECRET_KEY = os.getenv("SECRET_KEY", "boomboom123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Passlib/Bcrypt compatibility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# from fastapi.security import HTTPBearer
# oauth2_scheme = HTTPBearer() 

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from Backend.app import models
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise HTTPException(status_code=401)
    except: raise HTTPException(status_code=401)
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user: raise HTTPException(status_code=401)
    return user