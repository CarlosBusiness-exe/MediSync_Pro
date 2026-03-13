import pytest
from pydantic import ValidationError
from datetime import date, time

from schemas.patient_schema import PatientSchemaBase, PatientSchemaResponse, PatientSchemaAppointments
from schemas.appointment_schema import AppointmentSchemaResponse

def test_pt_schema_valid():
    data = {
        "name":"Josh",
        "age":22,
        "document_id":"963100162",
        "gender":"male",
        "email":"josh@gmail.com",
        "phone":"+13055331058",
        "historical":"Diabetic",
        "address":"Bourbon Street, 600, New Orleans, LA, 70130"
    }

    patient = PatientSchemaBase(**data)

    assert patient.name == "Josh"
    assert patient.phone == "+13055331058"
    assert isinstance(patient.phone, str)

def test_pt_invalid_types():
    data = {
        "name":"Josh",
        "age":"22",
        "document_id":963100162,
        "gender":"male",
        "email":"josh@gmail.com",
        "phone":13055331058,
        "historical":"Diabetic",
        "address":"Bourbon Street, 600, New Orleans, LA, 70130"
    }

    with pytest.raises(ValidationError):
        patient = PatientSchemaBase(**data)

def test_pt_missing_data():
    data = {
        "document_id":"963100162",
        "gender":"male",
        "email":"josh@gmail.com",
        "phone":"+13055331058",
        "historical":"Diabetic",
        "address":"Bourbon Street, 600, New Orleans, LA, 70130"
    }

    with pytest.raises(ValidationError):
        patient = PatientSchemaBase(**data)

def test_pt_schema_response():
    data = {
        "id":1,
        "name":"Josh",
        "age":22,
        "document_id":"963100162",
        "gender":"male",
        "email":"josh@gmail.com",
        "phone":"+13055331058",
        "historical":"Diabetic",
        "address":"Bourbon Street, 600, New Orleans, LA, 70130"
    }

    patient = PatientSchemaResponse(**data)

    assert patient.id == 1

def test_pt_ap_list():
    data = {
        "id":1,
        "name":"Josh",
        "age":22,
        "document_id":"963100162",
        "gender":"male",
        "email":"josh@gmail.com",
        "phone":"+13055331058",
        "historical":"Diabetic",
        "address":"Bourbon Street, 600, New Orleans, LA, 70130",
        "appointments":[
            {
                "id":99,
                "ap_date":"2026-03-10",
                "ap_time":"14:00:00",
                "doctor_id":1,
                "patient_id":1,
                "status":"Pending"
            },
            {
                "id":77,
                "ap_date":"2026-03-11",
                "ap_time":"15:00:00",
                "doctor_id":1,
                "patient_id":2,
                "status":"Pending"
            }
        ]
    }

    patient = PatientSchemaAppointments(**data)

    first_appointment = patient.appointments[0]
    assert first_appointment.id == 99
    assert first_appointment.patient_id == 1
    assert len(patient.appointments) == 2