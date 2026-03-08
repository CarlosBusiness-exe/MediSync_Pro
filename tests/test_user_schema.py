import pytest
from pydantic import ValidationError
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaResponse

def test_user_schema_valid():
    data = {
        "name": "Carl",
        "mail": "carl@gmail.com",
        "is_admin": True
    }
    
    user = UserSchemaBase(**data)
    
    assert user.name == "Carl"
    assert user.mail == "carl@gmail.com"
    assert user.is_admin is True

def test_user_schema_create_valid():
    data = {
        "name": "Carl",
        "mail": "carl@gmail.com",
        "is_admin": False,
        "password": "strongpassword123"
    }
    
    user = UserSchemaCreate(**data)
    
    assert user.password == "strongpassword123"
    assert user.is_admin is False

def test_user_invalid_types():
    data = {
        "name": "Carl",
        "mail": "carl@gmail.com",
        "is_admin": "not-a-boolean" 
    }
    
    with pytest.raises(ValidationError):
        UserSchemaBase(**data)

def test_user_missing_data():
    data = {
        "name": "Carl"
    }
    
    with pytest.raises(ValidationError):
        UserSchemaBase(**data)

def test_user_schema_response():
    data = {
        "id": 1,
        "name": "Carl",
        "mail": "carl@gmail.com",
        "is_admin": True
    }
    
    user = UserSchemaResponse(**data)
    
    assert user.id == 1
    assert not hasattr(user, "password")