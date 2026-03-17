import pytest
from fastapi import HTTPException, status
from sqlmodel import select

from core.configs import settings
from models.doctor_model import DoctorModel

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

def test_create_doctor_success(client, session, auth_headers):
    payload = {
        "name":"Carl",
        "crm":"017199/GO",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time": "08:00:00.893Z",
        "end_time": "17:00:00.893Z"
    }

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 201

    assert "id" in data
    assert "name" in data
    assert "crm" in data

    assert data["name"] == payload["name"]
    assert data["crm"] == payload["crm"]

    query = select(DoctorModel).where(DoctorModel.crm == payload["crm"])
    doctor_in_db = session.exec(query).first()
    assert doctor_in_db is not None
    assert doctor_in_db.name == payload["name"]
    assert doctor_in_db.crm == payload["crm"]

def test_create_doctor_missing(client, session, auth_headers):
    payload = {
        "name":"Carl",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289"
    }

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 422

    query = select(DoctorModel).where(DoctorModel.email == payload["email"])
    doctor_in_db = session.exec(query).first()
    assert doctor_in_db is None

def test_create_doctor_invalid(client, session, auth_headers):
    payload = {
        "name":7,
        "crm":"017199/GO",
        "specialty":10,
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time": 8,
        "end_time": 17
    }

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 422

    query = select(DoctorModel).where(DoctorModel.email == payload["email"])
    doctor_in_db = session.exec(query).first()
    assert doctor_in_db is None

def test_create_doctor_duplicate_crm(client, session, auth_headers):
    doctor1 = {
        "name":"Carl",
        "crm":"017199/GO",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289",
        "start_time": "08:00:00.893Z",
        "end_time": "17:00:00.893Z"
    }

    dt1_response = client.post(f"{settings.API_V1_STR}/doctors/", json=doctor1, headers=auth_headers)
    assert dt1_response.status_code == 201

    doctor2 = {
        "name":"Other Carl",
        "crm":"017199/GO",
        "specialty":"therapist",
        "email":"thercarl@gmail.com",
        "phone":"+13052335289",
        "start_time": "08:00:00.893Z",
        "end_time": "17:00:00.893Z"
    }

    dt2_response = client.post("api/v1/doctors/", json=doctor2, headers=auth_headers)

    assert dt2_response.status_code == 409
    assert dt2_response.json()["detail"] == "Already exist a doctor with this CRM."

    session.expire_all()

    query = select(DoctorModel).where(DoctorModel.crm == doctor1["crm"])
    results = session.exec(query).all()
    assert len(results) == 1
    assert results[0].email == doctor1["email"]
    assert results[0].name == doctor1["name"]

def test_get_invalid_id(client, auth_headers):
    invalid_id = 9999
    response = client.get(f"{settings.API_V1_STR}/doctors/{invalid_id}", headers=auth_headers)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found."

def test_create_without_token(client):
    payload = {
        "name": "Unauthorized Doc",
        "crm": "0000/GO",
        "specialty": "none",
        "email": "unauth@test.com",
        "phone": "000"
    }
    response = client.post("api/v1/doctors/", json=payload)
    
    assert response.status_code == 401

def test_get_empty(client, auth_headers):
    response = client.get(f"{settings.API_V1_STR}/doctors/", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0