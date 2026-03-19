from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from typing import List

from core.deps import get_session, get_current_user
from schemas.appointment_schema import AppointmentSchemaBase, AppointmentSchemaResponse
from services.appointment_service import AppointmentService
from models.user_model import UserModel
from core.authorization import RoleChecker
from schemas.user_schema import UserRole

router = APIRouter()

allow_admin = RoleChecker([UserRole.ADMIN])
allow_doctor = RoleChecker([UserRole.ADMIN, UserRole.DOCTOR])
allow_all = RoleChecker([UserRole.ADMIN, UserRole.DOCTOR, UserRole.PATIENT])

@router.post("/", response_model=AppointmentSchemaResponse, status_code=status.HTTP_201_CREATED)
def create_ap(appointment_data: AppointmentSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_doctor)):
    return AppointmentService.create_ap(appointment_data, db)

@router.get("/{appointment_id}", response_model=AppointmentSchemaResponse)
def get_ap_by_id(appointment_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_all)):
    return AppointmentService.get_ap_by_id(appointment_id, db)

@router.get("/", response_model=List[AppointmentSchemaResponse])
def get_all_ap(db: Session = Depends(get_session), current_user: UserModel = Depends(allow_all)):
    AppointmentService.auto_complete_past_appointments(db)
    return AppointmentService.get_all_ap(db)

@router.put("/{appointment_id}", response_model=AppointmentSchemaResponse)
def update_ap(appointment_id: int, appointment_data: AppointmentSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_doctor)):
    return AppointmentService.update_ap(appointment_id, appointment_data, db)

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ap(appointment_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_admin)):
    return AppointmentService.delete_ap(appointment_id, db)

@router.patch("/complete/{appointment_id}", response_model=AppointmentSchemaResponse)
def complete_appointment(appointment_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_admin)):
    return AppointmentService.complete_appointment(appointment_id, db)