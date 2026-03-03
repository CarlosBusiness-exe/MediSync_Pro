from typing import Optional, List

from sqlmodel import SQLModel, Field

from schemas.appointment_schema import AppointmentSchemaResponse

class PatientSchemaBase(SQLModel):
    name: str
    age: int
    document_id: str = Field(index=True, unique=True)
    gender: str
    mail: str
    phone: str
    historical: Optional[str] = None
    address: Optional[str] = None

class PatientSchemaResponse(PatientSchemaBase):
    id: int

class PatientSchemasAppointments(PatientSchemaResponse):
    appointments: List[AppointmentSchemaResponse] = []