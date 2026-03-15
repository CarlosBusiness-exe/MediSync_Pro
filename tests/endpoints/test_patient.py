import pytest
from fastapi import HTTPException, status
from sqlmodel import select

from core.configs import settings
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

def test_create_patient_success(client, session, auth_headers):
    payload = {
        "name":"Jhon",
        "age":20,
        "document_id":"76598712308",
        "gender":"male",
        "email":"jhon@gmail.com",
        "phone":"64982637263",
        "historical":"diabetic",
        "address":"Street A"
    }

    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 201

    assert "id" in data
    assert "name" in data
    assert "document_id" in data

    assert data["name"] == payload["name"]
    assert data["document_id"] == payload["document_id"]

    query = select(PatientModel).where(PatientModel.document_id == payload["document_id"])
    patient_in_db = session.exec(query).first()
    assert patient_in_db is not None
    assert patient_in_db.name == payload["name"]

def test_create_patient_missing(client, session, auth_headers):
    payload = {
        "age":20,
        "gender":"male",
        "email":"jhon@gmail.com",
        "historical":"diabetic",
        "address":"Street A"
    }
    
    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 422

    query = select(PatientModel).where(PatientModel.email == payload["email"])
    patient_in_db = session.exec(query).first()
    assert patient_in_db is None

def test_create_patient_invalid(client, session, auth_headers):
    payload = {
        "name":999,
        "age":"string",
        "document_id":76598712308,
        "gender":"male",
        "email":"jhon@gmail.com",
        "phone":"64982637263",
        "historical":"diabetic",
        "address":"Street A"
    }

    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload, headers=auth_headers)
    data = response.json()

    assert response.status_code == 422

    query = select(PatientModel).where(PatientModel.email == payload["email"])
    patient_in_db = session.exec(query).first()
    assert patient_in_db is None

def test_create_patient_duplicated_doc(client, session, auth_headers):
    patient1 = {
        "name":"Jhon",
        "age":20,
        "document_id":"76598712308",
        "gender":"male",
        "email":"jhon@gmail.com",
        "phone":"64982637263",
        "historical":"diabetic",
        "address":"Street A"
    }

    response_dt1 = client.post(f"{settings.API_V1_STR}/patients/", json=patient1, headers=auth_headers)
    assert response_dt1.status_code == 201

    patient2 = {
        "name":"Jazz",
        "age":24,
        "document_id":"76598712308",
        "gender":"male",
        "email":"jazz@gmail.com",
        "phone":"64982637263",
        "historical":"diabetic",
        "address":"Street A"
    }

    response_dt2 = client.post(f"{settings.API_V1_STR}/patients/", json=patient2, headers=auth_headers)
    assert response_dt2.status_code == 409
    assert response_dt2.json()["detail"] == "Already exist a patient with this document id."

    session.expire_all()

    query = select(PatientModel).where(PatientModel.document_id == patient1["document_id"])
    results = session.exec(query).all()
    assert len(results) == 1
    assert results[0].email == patient1["email"]
    assert results[0].name == patient1["name"]

def test_get_invalid_id(client, session, auth_headers):
    invalid_id = 9999
    response = client.get(f"{settings.API_V1_STR}/patients/{invalid_id}", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found."

def test_create_without_token(client):
    payload = {
        "name":"Jhon",
        "age":20,
        "document_id":"76598712308",
        "gender":"male",
        "email":"jhon@gmail.com",
        "phone":"64982637263",
        "historical":"diabetic",
        "address":"Street A"
    }
    response = client.post("api/v1/doctors/", json=payload)
    
    assert response.status_code == 401

def test_get_empty(client, auth_headers):
    response = client.get(f"{settings.API_V1_STR}/patients/", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0