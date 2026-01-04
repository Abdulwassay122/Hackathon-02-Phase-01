from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import engine
from contextlib import contextmanager
from src.config import settings

# Create database engine
connection_string = str(settings.database_url)
engine = create_engine(connection_string, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session