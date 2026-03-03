from typing import List

from sqlmodel import SQLModel, Field

from schemas.appointment_schema import AppointmentSchemaResponse

class DoctorSchemaBase(SQLModel):
    name: str
    crm: str = Field(unique=True, index=True)
    specialty: str = Field(index=True)
    mail: str
    phone: str

class DoctorSchemaResponse(DoctorSchemaBase):
    id: int

class DoctorSchemaAppointments(DoctorSchemaResponse):
    appointments: List[AppointmentSchemaResponse] = []