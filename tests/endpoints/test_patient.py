import pytest
from fastapi import HTTPException, status
from sqlmodel import select

from core.configs import settings
from models.patient_model import PatientModel

def test_create_patient_success(client, session):
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

    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload)
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

def test_create_patient_missing(client, session):
    payload = {
        "age":20,
        "gender":"male",
        "email":"jhon@gmail.com",
        "historical":"diabetic",
        "address":"Street A"
    }
    
    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload)
    data = response.json()

    assert response.status_code == 422

    query = select(PatientModel).where(PatientModel.email == payload["email"])
    patient_in_db = session.exec(query).first()
    assert patient_in_db is None

def test_create_patient_invalid(client, session):
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

    response = client.post(f"{settings.API_V1_STR}/patients/", json=payload)
    data = response.json()

    assert response.status_code == 422

    query = select(PatientModel).where(PatientModel.email == payload["email"])
    patient_in_db = session.exec(query).first()
    assert patient_in_db is None

def test_create_patient_duplicated_doc(client, session):
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

    response_dt1 = client.post(f"{settings.API_V1_STR}/patients/", json=patient1)
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

    response_dt2 = client.post(f"{settings.API_V1_STR}/patients/", json=patient2)
    assert response_dt2.status_code == 409
    assert response_dt2.json()["detail"] == "Already exist a patient with this document id."

    session.expire_all()

    query = select(PatientModel).where(PatientModel.document_id == patient1["document_id"])
    results = session.exec(query).all()
    assert len(results) == 1
    assert results[0].email == patient1["email"]
    assert results[0].name == patient1["name"]

def test_get_invalid_id(client, session):
    invalid_id = 9999
    response = client.get(f"{settings.API_V1_STR}/patients/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found."

def test_get_empty(client):
    response = client.get(f"{settings.API_V1_STR}/patients/")

    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0