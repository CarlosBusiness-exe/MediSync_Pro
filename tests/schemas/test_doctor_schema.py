import pytest
from pydantic import ValidationError
from datetime import date, time

from schemas.doctor_schema import DoctorSchemaBase, DoctorSchemaResponse, DoctorSchemaAppointments
from schemas.appointment_schema import AppointmentSchemaResponse

def test_dt_schema_valid():
    data = {
        "user_id":1,
        "name":"Carl",
        "crm":"017199",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time":"18:50:59.426Z",
        "end_time":"18:51:26.082Z"
    }

    doctor = DoctorSchemaBase(**data)

    assert doctor.name == "Carl"
    assert doctor.phone == "+13055335289"
    assert isinstance(doctor.start_time, time)
    assert isinstance(doctor.phone, str)

def test_dt_invalid_types():
    data = {
        "name":9,
        "crm":"017199",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":13055335289,
        "start_time":8,
        "end_time":17
    }

    with pytest.raises(ValidationError):
        doctor = DoctorSchemaBase(**data)

def test_dt_missing_data():
    data = {
        "name":"Carl",
        "email":"carl@gmail.com",
        "phone":"+13055335289"
    }

    with pytest.raises(ValidationError):
        doctor = DoctorSchemaBase(**data)

def test_dt_schema_response():
    data = {
        "user_id":1,
        "id":1,
        "name":"Carl",
        "crm":"017199",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time":"18:50:59.426Z",
        "end_time":"18:51:26.082Z"
    }

    doctor = DoctorSchemaResponse(**data)

    assert doctor.id == 1

def test_dt_ap_list():
    data = {
        "user_id":1,
        "id":1,
        "name":"Carl",
        "crm":"017199",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time":"18:50:59.426Z",
        "end_time":"18:51:26.082Z",
        "appointments":[
            {
                "id":99,
                "ap_date":"2026-03-10",
                "ap_time":"14:00:00",
                "doctor_id":1,
                "patient_id":1,
                "status":"Pending",
                "is_active":True
            },
            {
                "id":77,
                "ap_date":"2026-03-11",
                "ap_time":"15:00:00",
                "doctor_id":1,
                "patient_id":2,
                "status":"Pending",
                "is_active":True
            }
        ]
    }

    doctor = DoctorSchemaAppointments(**data)

    first_appointment = doctor.appointments[0]
    assert first_appointment.id == 99
    assert first_appointment.doctor_id == 1
    assert len(doctor.appointments) == 2