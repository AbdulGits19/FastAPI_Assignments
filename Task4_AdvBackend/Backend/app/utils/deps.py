# Backend/app/utils/deps.py
from fastapi import Depends, HTTPException, status
from Backend.app.core_auth import get_current_active_user 
from Backend.app.models import User

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {self.allowed_roles}"
            )
        return user

# Shortcut Helpers
is_admin = RoleChecker(["Admin"])
is_doctor_or_admin = RoleChecker(["Doctor", "Admin"])
# ADD THIS LINE:
is_any_user = RoleChecker(["Admin", "Doctor", "Patient"])