from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
from typing import Optional
from core.configs import settings
import jwt
from fastapi import Depends, HTTPException, status
from schemas.user_schema import UserRole
from models.user_model import UserModel
from core.deps import get_current_user
from typing import List

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

def create_access_token(email: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": email}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

class RoleCheker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserModel = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted for your user role.")
        return user