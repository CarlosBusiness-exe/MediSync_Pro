from typing import Optional
from sqlmodel import SQLModel
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

class UserSchemaBase(SQLModel):
    name: str
    email: str
    is_admin: bool
    role: UserRole

class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaResponse(UserSchemaBase):
    id: int