from sqlmodel import SQLModel
from core.database import engine
import models

def create_tables() -> None:
    print("The tables are being created...")
    
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    print("The tables have been created")

if __name__ == "__main__":
    create_tables()