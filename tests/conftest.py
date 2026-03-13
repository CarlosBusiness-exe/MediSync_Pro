import pytest
from sqlmodel import create_engine, Session, SQLModel
from fastapi.testclient import TestClient

from main import app
from core.deps import get_session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
        
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()