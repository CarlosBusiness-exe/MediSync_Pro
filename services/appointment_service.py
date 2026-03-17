from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException, status

from schemas.appointment_schema import AppointmentSchemaBase
from models.appointment_model import AppointmentModel
from services.doctor_service import DoctorService
from services.patient_service import PatientService

class AppointmentService:
    @staticmethod
    def create_ap(appointment_data: AppointmentSchemaBase, db: Session):
        #Cheking if Doctor and Patient exist
        DoctorService.get_doctor_by_id(appointment_data.doctor_id, db)
        PatientService.get_patient_by_id(appointment_data.patient_id, db)

        #Prevent doble bookings
        query = select(AppointmentModel).where(AppointmentModel.ap_date == appointment_data.ap_date, AppointmentModel.ap_time == appointment_data.ap_time, (AppointmentModel.doctor_id == appointment_data.doctor_id) | (AppointmentModel.patient_id == appointment_data.patient_id), AppointmentModel.is_active == True)
        appointment_up = db.exec(query).first()
        if appointment_up:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor or Patient already has an appointment scheduled at this time.")
        
        new_appointment = AppointmentModel(**appointment_data.model_dump())
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        return new_appointment
    
    @staticmethod
    def get_ap_by_id(appointment_id: int, db: Session):
        query = select(AppointmentModel).where(AppointmentModel.id == appointment_id)
        appointment = db.exec(query).first()

        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")

        return appointment
    
    @staticmethod
    def get_all_ap(db: Session):
        query = select(AppointmentModel)
        appointments = db.exec(query).all()

        return appointments
    
    @staticmethod
    def update_ap(appointment_id: int, appointment_data: AppointmentSchemaBase, db: Session):
        appointment_up = AppointmentService.get_ap_by_id(appointment_id, db)

        appointment_data_dict = appointment_data.model_dump(exclude_unset=True)
        appointment_up.sqlmodel_update(appointment_data_dict)

        db.commit()
        db.refresh(appointment_up)

        return appointment_up
    
    @staticmethod
    def delete_ap(appointment_id: int, db: Session):
        appointment_up = AppointmentService.get_ap_by_id(appointment_id, db)

        appointment_up.is_active = False
        db.commit()

        return None
    
    @staticmethod
    def complete_appointment(appointment_id: int, db: Session):
        appointment = AppointmentService.get_ap_by_id(appointment_id, db)
        
        appointment.status = "Completed"
        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return appointment
    
    #Add this to the scheduling page to update.
    @staticmethod
    def auto_complete_past_appointments(db: Session):
        now = datetime.now()
        query = select(AppointmentModel).where(
            AppointmentModel.status == "Pending",
            (AppointmentModel.ap_date < now.date()) | 
            ((AppointmentModel.ap_date == now.date()) & (AppointmentModel.ap_time < now.time()))
        )
        
        past_appointments = db.exec(query).all()
        for ap in past_appointments:
            ap.status = "Completed"
            db.add(ap)
        
        db.commit()