from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Optional

from core.configs import settings
from models.user_model import UserModel
from core.security import verify_password, DUMMY_HASH

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")

def authenticate_user(db: Session, mail: str, password: str):
    query = select(UserModel).where(UserModel.mail == mail)
    user = db.exec(query).first()

    if not user:
        verify_password(password, DUMMY_HASH)
        return None
        
    if not verify_password(password, user.password): 
        return None
        
    return user