from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from schemas.doctor_schema import DoctorSchemaBase

if TYPE_CHECKING:
    from models.appointment_model import AppointmentModel

class DoctorModel(DoctorSchemaBase, table=True):
    __tablename__ = "doctors"

    id: Optional[int] = Field(default=None, primary_key=True)

    appointments: List["AppointmentModel"] = Relationship(back_populates="doctor")