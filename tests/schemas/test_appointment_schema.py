import pytest
from pydantic import ValidationError
from datetime import date, time

from schemas.appointment_schema import AppointmentSchemaBase, AppointmentSchemaResponse

def test_ap_schema_valid():
    data = {
        "ap_date":"2026-03-10",
        "ap_time":"14:00:00",
        "doctor_id":1,
        "patient_id":1,
        "status":"Pending",
        "is_active":True
    }

    appointment = AppointmentSchemaBase(**data)

    assert appointment.doctor_id == 1
    assert isinstance(appointment.ap_date, date)

def test_ap_schema_invalid_types():
    data = {
        "ap_date":"string",
        "ap_time":"14:00:00",
        "doctor_id":"string",
        "patient_id":1,
        "status":0,
        "is_active":"True"
    }

    with pytest.raises(ValidationError):
        AppointmentSchemaBase(**data)

def test_ap_schema_missing_data():
    data = {
        "ap_date":"2026-03-10",
        "ap_time":"14:00:00",
        "status":"Pending"
    }

    with pytest.raises(ValidationError):
        AppointmentSchemaBase(**data)

def test_ap_schema_response():
    data = {
        "id":99,
        "ap_date":"2026-03-10",
        "ap_time":"14:00:00",
        "doctor_id":1,
        "patient_id":1,
        "status":"Pending"
    }

    response = AppointmentSchemaResponse(**data)

    assert response.id == 99