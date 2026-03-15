from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from models.user_model import UserModel
from core.deps import get_current_user
from core.security import get_password_hash, create_access_token
from core.auth import authenticate_user
from schemas.user_schema import UserSchemaBase, UserSchemaCreate

class UserService:
    @staticmethod
    def get_logged(logged_user: UserModel):
        return logged_user
    
    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm, db: Session):
        user = authenticate_user(db, email=form_data.username, password=form_data.password)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The data is incorrect")
        
        return {"access_token": create_access_token(user.email), "token_type": "bearer"}
    
    #Create/Signup user
    @staticmethod
    def post_user(user_data: UserSchemaCreate, db: Session):
        #Prevent duplicated email
        query = select(UserModel).where(UserModel.email == user_data.email)
        user_up = db.exec(query).first()
        if user_up:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email address already exists.")
        
        new_user = UserModel.model_validate(user_data)
        new_user.password = get_password_hash(new_user.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def get_all_users(db: Session):
        query = select(UserModel)
        users = db.exec(query).all()

        return users
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        query = select(UserModel).where(UserModel.id == user_id)
        user = db.exec(query).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        return user
    
    @staticmethod
    def update_user(user_id: int, user_data: UserSchemaCreate, db: Session):
        user_up = UserService.get_user_by_id(user_id, db)

        user_data_dict = user_data.model_dump(exclude_unset=True)

        if "password" in user_data_dict:
            user_data_dict["password"] = get_password_hash(user_data_dict["password"])

        user_up.sqlmodel_update(user_data_dict)

        db.commit()
        db.refresh(user_up)

        return user_up
    
    @staticmethod
    def delete_user(user_id: int, db: Session):
        user_del = UserService.get_user_by_id(user_id, db)

        db.delete(user_del)
        db.commit()

        return None