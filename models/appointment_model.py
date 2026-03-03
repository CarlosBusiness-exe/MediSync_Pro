from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from schemas.appointment_schema import AppointmentSchemaBase

if TYPE_CHECKING:
    from models.doctor_model import DoctorModel
    from models.patient_model import PatientModel

class AppointmentModel(AppointmentSchemaBase, table=True):
    __tablename__ = "appointments"

    id: Optional[int] = Field(default=None, primary_key=True)

    doctor_id: int = Field(foreign_key="doctors.id")
    patient_id: int = Field(foreign_key="patients.id")

    doctor: Optional["DoctorModel"] = Relationship(back_populates="appointments")
    patient: Optional["PatientModel"] = Relationship(back_populates="appointments")