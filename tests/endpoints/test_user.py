import pytest
from sqlmodel import select
from core.configs import settings
from models.user_model import UserModel

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

def test_post_user_success(client, session, user_data):
    response = client.post(f"{settings.API_V1_STR}/users/signup", json=user_data)
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == user_data["email"]
    
    query = select(UserModel).where(UserModel.email == user_data["email"])
    user_db = session.exec(query).first()
    assert user_db is not None
    assert user_db.name == user_data["name"]

def test_post_user_duplicate_email(client, created_user, user_data):
    response = client.post(f"{settings.API_V1_STR}/users/signup", json=user_data)
    
    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email address already exists."

def test_login_success(client, created_user, user_data):
    login_payload = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post(f"{settings.API_V1_STR}/users/login", data=login_payload)
    data = response.json()

    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert "access_token" in data

def test_get_logged_user(client, user_token, created_user):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"{settings.API_V1_STR}/users/logged", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["id"] == created_user["id"]

def test_update_user_with_password(client, created_user):
    user_id = created_user["id"]
    update_data = {
        "name": "Carl Updated",
        "email": "carl.updated@example.com",
        "password": "newsecurepassword",
        "is_admin": True
    }
    response = client.put(f"{settings.API_V1_STR}/users/{user_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Carl Updated"

def test_delete_user_success(client, session, created_user):
    user_id = created_user["id"]
    response = client.delete(f"{settings.API_V1_STR}/users/{user_id}")
    
    assert response.status_code == 204
    
    query = select(UserModel).where(UserModel.id == user_id)
    assert session.exec(query).first() is None