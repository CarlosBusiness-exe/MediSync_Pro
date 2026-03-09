from sqlmodel import Session, select
from schemas.doctor_schema import DoctorSchemaBase
from models.doctor_model import DoctorModel
from fastapi import HTTPException, status

class DoctorService:
    @staticmethod
    def create_doctor(doctor_data: DoctorSchemaBase, db: Session):
        #Prevent duplicated CRM
        query = select(DoctorModel).where(DoctorModel.crm == doctor_data.crm)
        doctor_up = db.exec(query).first()
        if doctor_up:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exist a doctor with this CRM.")

        new_doctor = DoctorModel(**doctor_data.model_dump())
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)
        return new_doctor
    
    @staticmethod
    def get_doctor_by_id(doctor_id: int, db: Session):
        query = select(DoctorModel).where(DoctorModel.id == doctor_id)
        doctor = db.exec(query).first()

        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
        
        return doctor
    
    @staticmethod
    def get_all_doctors(db: Session):
        query = select(DoctorModel)
        doctors = db.exec(query).all()

        return doctors
    
    @staticmethod
    def update_doctor(doctor_id: int, doctor_data: DoctorSchemaBase, db: Session):
        query = select(DoctorModel).where(DoctorModel.id == doctor_id)
        doctor_up = db.exec(query).first()

        if not doctor_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
        
        doctor_data_dict = doctor_data.model_dump(exclude_unset=True)
        doctor_up.sqlmodel_update(doctor_data_dict)

        db.commit()
        db.refresh(doctor_up)

        return doctor_up
    
    @staticmethod
    def delete_doctor(doctor_id: int, db: Session):
        doctor_del = DoctorService.get_doctor_by_id(doctor_id, db)
        
        db.delete(doctor_del)
        db.commit()