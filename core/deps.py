from typing import Generator, Optional

from fastapi import Depends
from sqlmodel import Session

from core.database import engine

def get_session() -> Generator:
    with Session(engine) as session:
        yield session