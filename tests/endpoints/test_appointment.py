import pytest
from fastapi import HTTPException, status
from sqlmodel import select

from core.configs import settings
from models.appointment_model import AppointmentModel
from models.doctor_model import DoctorModel
from models.patient_model import PatientModel

@pytest.fixture
def user_data():
    return {
        "name": "Carl",
        "email": "carl.dev@example.com",
        "password": "strongpassword123",
        "is_admin": True
    }

@pytest.fixture
def created_user(client, user_data):
    response = client.post(f"{settings.API_V1_STR}/users/signup", json=user_data)
    return response.json()

@pytest.fixture
def user_token(client, user_data, created_user):
    login_payload = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post(f"{settings.API_V1_STR}/users/login", data=login_payload)
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
def created_doctor(client, auth_headers):
    doctor = {
        "name": "Carl", "crm": "017199/GO", "specialty": "cardiologist",
        "email": "carl@gmail.com", "phone": "+13055335289"
    }
    response = client.post(f"{settings.API_V1_STR}/doctors/", json=doctor, headers=auth_headers)
    return response.json()

@pytest.fixture
def created_patient(client, auth_headers):
    patient = {
        "name": "Jhon", "age": 20, "document_id": "76598712308", "gender": "male",
        "email": "jhon@gmail.com", "phone": "64982637263", "historical": "diabetic", "address": "Street A"
    }
    response = client.post(f"{settings.API_V1_STR}/patients/", json=patient, headers=auth_headers)
    return response.json()

def test_create_ap_success(client, session, created_doctor, created_patient, auth_headers):
    appointment = {
        "ap_date": "2026-03-30",
        "ap_time": "13:00:00",
        "doctor_id": created_doctor["id"],
        "patient_id": created_patient["id"],
        "status": "Pending"
    }

    response = client.post(f"{settings.API_V1_STR}/appointments/", json=appointment, headers=auth_headers)
    data = response.json()
    assert response.status_code == 201

    assert "id" in data
    assert "doctor_id" in data
    assert "patient_id" in data

    assert data["doctor_id"] == created_doctor["id"]
    assert data["patient_id"] == created_patient["id"]

    query = select(AppointmentModel).where(AppointmentModel.id == data["id"])
    appointment_in_db = session.exec(query).first()
    assert appointment_in_db.doctor_id == created_doctor["id"]
    assert appointment_in_db.patient_id == created_patient["id"]

def test_create_ap_missing(client, created_patient, auth_headers):
    payload = {
        "ap_time": "13:00:00",
        "patient_id": created_patient["id"],
        "status": "Pending"
    }

    response = client.post(f"{settings.API_V1_STR}/appointments/", json=payload, headers=auth_headers)
    assert response.status_code == 422

def test_create_ap_invalid(client, created_patient, auth_headers):
    appointment = {
        "ap_date":"2026,03,30",
        "ap_time":"13,00,00",
        "doctor_id":"string",
        "patient_id":created_patient["id"],
        "status":"Pending"
    }

    response = client.post(f"{settings.API_V1_STR}/appointments/", json=appointment, headers=auth_headers)
    assert response.status_code == 422

def test_create_ap_same_time(client, created_doctor, created_patient, auth_headers):
    appointment = {
        "ap_date":"2026-03-30",
        "ap_time":"13:00:00",
        "doctor_id": created_doctor["id"],
        "patient_id": created_patient["id"],
        "status":"Pending"
    }

    response = client.post(f"{settings.API_V1_STR}/appointments/", json=appointment, headers=auth_headers)
    data = response.json()
    assert response.status_code == 201

    same_time_ap = {
        "ap_date":"2026-03-30",
        "ap_time":"13:00:00",
        "doctor_id": created_doctor["id"],
        "patient_id": created_patient["id"],
        "status":"Pending"
    }

    st_response = client.post(f"{settings.API_V1_STR}/appointments/", json=same_time_ap, headers=auth_headers)
    data = st_response.json()

    assert st_response.status_code == 400
    assert data["detail"] == "Doctor or Patient already has an appointment scheduled at this time."

def test_get_invalid_id(client, auth_headers):
    invalid_id = 9999

    response = client.get(f"{settings.API_V1_STR}/appointments/{invalid_id}", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found."

def test_create_without_token(client, created_doctor, created_patient):
    appointment = {
        "ap_date": "2026-03-30",
        "ap_time": "13:00:00",
        "doctor_id": created_doctor["id"],
        "patient_id": created_patient["id"],
        "status": "Pending"
    }
    response = client.post("api/v1/doctors/", json=appointment)
    
    assert response.status_code == 401

def test_get_empty(client, auth_headers):
    response = client.get(f"{settings.API_V1_STR}/appointments/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0