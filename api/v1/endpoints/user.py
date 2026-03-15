from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List

from core.deps import get_session, get_current_user
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaResponse
from models.user_model import UserModel
from services.user_service import UserService

router = APIRouter()

@router.get("/logged", response_model=UserSchemaResponse)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    return UserService.login(form_data, db)

@router.post("/signup", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED)
def post_user(user_data: UserSchemaCreate, db: Session = Depends(get_session)):
    return UserService.post_user(user_data, db)

@router.get("/", response_model=List[UserSchemaResponse])
def get_all_users(db: Session = Depends(get_session)):
    return UserService.get_all_users(db)

@router.get("/{user_id}", response_model=UserSchemaResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_session)):
    return UserService.get_user_by_id(user_id, db)

@router.put("/{user_id}", response_model=UserSchemaResponse)
def update_user(user_id: int, user_data: UserSchemaCreate, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return UserService.update_user(user_id, user_data, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return UserService.delete_user(user_id, db)