from sqlmodel import SQLModel, Field

from datetime import date, time

class AppointmentSchemaBase(SQLModel):
    ap_date: date = Field(index=True)
    ap_time: time = Field(index=True)
    doctor_id: int = Field(index=True)
    patient_id: int
    status: str = "Pending"
    is_active: bool = True

class AppointmentSchemaResponse(AppointmentSchemaBase):
    id: int