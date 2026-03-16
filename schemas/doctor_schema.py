from typing import List
from datetime import time

from sqlmodel import SQLModel, Field

from schemas.appointment_schema import AppointmentSchemaResponse

class DoctorSchemaBase(SQLModel):
    name: str
    crm: str = Field(unique=True, index=True)
    specialty: str = Field(index=True)
    email: str
    phone: str
    start_time: time = Field(index=True, default=None)
    end_time: time = Field(index=True, default=None)

class DoctorSchemaResponse(DoctorSchemaBase):
    id: int

class DoctorSchemaAppointments(DoctorSchemaResponse):
    appointments: List[AppointmentSchemaResponse] = []