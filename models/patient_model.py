from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from schemas.patient_schema import PatientSchemaBase

if TYPE_CHECKING:
    from models.appointment_model import AppointmentModel

class PatientModel(PatientSchemaBase, table=True):
    __tablename__ = "patients"

    id: Optional[int] = Field(default=None, primary_key=True)

    appointments: List["AppointmentModel"] = Relationship(back_populates="patient")