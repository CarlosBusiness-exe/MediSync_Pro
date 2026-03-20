from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from schemas.user_schema import UserSchemaBase

if TYPE_CHECKING:
    from models.doctor_model import DoctorModel 
    from models.patient_model import PatientModel

class UserModel(UserSchemaBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str

    doctor_profile: Optional["DoctorModel"] = Relationship(back_populates="user")
    patient_profile: Optional["PatientModel"] = Relationship(back_populates="user")