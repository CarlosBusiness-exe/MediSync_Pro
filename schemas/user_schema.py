from typing import Optional
from sqlmodel import SQLModel

class UserSchemaBase(SQLModel):
    name: str
    mail: str
    is_admin: bool

class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaResponse(UserSchemaBase):
    id: int