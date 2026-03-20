from sqlmodel import Session, select
from schemas.patient_schema import PatientSchemaBase
from models.patient_model import PatientModel
from models.user_model import UserModel
from schemas.user_schema import UserRole
from fastapi import HTTPException, status

class PatientService:
    @staticmethod
    def create_patient(patient_data: PatientSchemaBase, db: Session):
        #Prevent duplicated document_id
        query = select(PatientModel).where(PatientModel.document_id == patient_data.document_id)
        patient_up = db.exec(query).first()
        if patient_up:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exist a patient with this document id.")
        
        new_patient = PatientModel(**patient_data.model_dump())
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return new_patient
    
    @staticmethod
    def get_patient_by_id(patient_id: int, db: Session, user: UserModel):
        if user.role not in [UserRole.ADMIN, UserRole.DOCTOR]:
            if user.id != patient_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't access this datas.")

        query = select(PatientModel).where(PatientModel.id == patient_id)
        patient = db.exec(query).first()

        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
        
        return patient
    
    @staticmethod
    def get_all_patients(db: Session):
        query = select(PatientModel)
        patients = db.exec(query).all()

        return patients
    
    @staticmethod
    def update_patient(patient_id: int, patient_data: PatientSchemaBase, db: Session, user: UserModel):
        patient_up = PatientService.get_patient_by_id(patient_id, db, user)

        patient_data_dict = patient_data.model_dump(exclude_unset=True)
        patient_up.sqlmodel_update(patient_data_dict)

        db.commit()
        db.refresh(patient_up)

        return patient_up

    @staticmethod
    def delete_patient(patient_id: int, db: Session, user: UserModel):
        patient_del = PatientService.get_patient_by_id(patient_id, db, user)

        db.delete(patient_del)
        db.commit()

        return None