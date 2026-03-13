import pytest
from fastapi import HTTPException, status
from sqlmodel import select

from core.configs import settings
from models.doctor_model import DoctorModel

def test_create_doctor_success(client, session):
    payload = {
        "name":"Carl",
        "crm":"017199/GO",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289"
    }

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload)
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

def test_create_doctor_missing(client, session):
    payload = {"name": "Carl"}

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload)
    data = response.json()

    assert response.status_code == 422

    query = select(DoctorModel).where(DoctorModel.email == payload["email"])
    doctor_in_db = session.exec(query).first()
    assert doctor_in_db is None

def test_create_doctor_invalid(client, session):
    payload = {
        "name":7,
        "crm":"017199/GO",
        "specialty":10,
        "email":"carl@gmail.com",
        "phone":"+13055335289"
    }

    response = client.post(f"{settings.API_V1_STR}/doctors/", json=payload)
    data = response.json()

    assert response.status_code == 422

    query = select(DoctorModel).where(DoctorModel.email == payload["email"])
    doctor_in_db = session.exec(query).first()
    assert doctor_in_db is None

def test_create_doctor_duplicate_crm(client, session):
    doctor1 = {
        "name":"Carl",
        "crm":"017199/GO",
        "specialty":"cardiologist",
        "email":"carl@gmail.com",
        "phone":"+13055335289"
    }

    dt1_response = client.post(f"{settings.API_V1_STR}/doctors/", json=doctor1)
    assert dt1_response.status_code == 201

    doctor2 = {
        "name":"Other Carl",
        "crm":"017199/GO",
        "specialty":"therapist",
        "email":"thercarl@gmail.com",
        "phone":"+13052335289"
    }

    dt2_response = client.post("api/v1/doctors/", json=doctor2)

    assert dt2_response.status_code == 409
    assert dt2_response.json()["detail"] == "Already exist a doctor with this CRM."

    session.expire_all()

    query = select(DoctorModel).where(DoctorModel.crm == doctor1["crm"])
    results = session.exec(query).all()
    assert len(results) == 1
    assert results[0].email == doctor1["email"]
    assert results[0].name == doctor1["name"]

def test_get_invalid_id(client):
    invalid_id = 9999
    response = client.get(f"{settings.API_V1_STR}/doctors/{invalid_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found."
"""
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
"""
def test_get_empty(client):
    response = client.get(f"{settings.API_V1_STR}/doctors/")
    
    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0