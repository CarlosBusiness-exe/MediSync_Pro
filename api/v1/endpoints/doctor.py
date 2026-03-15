from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from typing import List

from core.deps import get_session, get_current_user
from schemas.doctor_schema import DoctorSchemaBase, DoctorSchemaResponse, DoctorSchemaAppointments
from services.doctor_service import DoctorService
from models.user_model import UserModel

router = APIRouter()

@router.post("/", response_model=DoctorSchemaResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor_data: DoctorSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return DoctorService.create_doctor(doctor_data, db)

@router.get("/{doctor_id}", response_model=DoctorSchemaResponse)
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return DoctorService.get_doctor_by_id(doctor_id, db)

@router.get("/", response_model=List[DoctorSchemaResponse])
def get_all_doctors(db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return DoctorService.get_all_doctors(db)

@router.put("/{doctor_id}", response_model=DoctorSchemaResponse)
def update_doctor(doctor_id: int, doctor_data: DoctorSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return DoctorService.update_doctor(doctor_id, doctor_data, db)

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    return DoctorService.delete_doctor(doctor_id, db)