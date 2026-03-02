from sqlmodel import create_engine
from sqlmodel import Session

from core.configs import settings

engine = create_engine(settings.DB_URL, echo=True)