from typing import Generator, Optional, Annotated

from fastapi import Depends, status, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
import jwt

from core.database import engine
from core.auth import oauth2_schema
from core.configs import settings
from models.user_model import UserModel

def get_session() -> Generator:
    with Session(engine) as session:
        yield session

class TokenData(BaseModel):
    username: Optional[str] = None

def get_user(db: Session, username: str):
    query = select(UserModel).where(UserModel.email == username)
    user = db.exec(query).first()

    return user

def get_current_user(token: Annotated[str, Depends(oauth2_schema)], db: Session = Depends(get_session)):
    credential_exception: HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The credential could not be authenticated.", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except Exception:
        raise credential_exception
    
    user: UserModel = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user