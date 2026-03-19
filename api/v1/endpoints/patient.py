from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from typing import List

from core.deps import get_session, get_current_user
from schemas.patient_schema import PatientSchemaBase, PatientSchemaResponse, PatientSchemaAppointments
from services.patient_service import PatientService
from models.user_model import UserModel
from core.authorization import RoleChecker
from schemas.user_schema import UserRole

router = APIRouter()

allow_admin = RoleChecker([UserRole.ADMIN])
allow_all = RoleChecker([UserRole.ADMIN, UserRole.PATIENT, UserRole.DOCTOR])


@router.post("/", response_model=PatientSchemaResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient_data: PatientSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_admin)):
    return PatientService.create_patient(patient_data, db)

@router.get("/{patient_id}", response_model=PatientSchemaResponse)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_all)): 
    return PatientService.get_patient_by_id(patient_id, db)

@router.get("/", response_model=List[PatientSchemaResponse])
def get_all_patients(db: Session = Depends(get_session), current_user: UserModel = Depends(allow_all)):
    return PatientService.get_all_patients(db)

@router.put("/{patient_id}", response_model=PatientSchemaResponse)
def update_patient(patient_id: int, patient_data: PatientSchemaBase, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_admin)):
    return PatientService.update_patient(patient_id, patient_data, db)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_session), current_user: UserModel = Depends(allow_admin)):
    return PatientService.delete_patient(patient_id, db)