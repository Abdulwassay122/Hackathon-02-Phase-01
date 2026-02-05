import pytest
from sqlmodel import Session, select
from src.database.connection import engine, get_session
from src.models.task import Task
from src.models.user import User
from unittest.mock import patch
import os


def test_postgresql_engine_creation():
    """Test that the PostgreSQL engine is created properly"""
    assert engine is not None
    assert "postgresql" in str(engine.url)


def test_session_creation():
    """Test that database sessions can be created"""
    try:
        with next(get_session()) as session:
            assert session is not None
    except Exception as e:
        pytest.fail(f"Failed to create database session: {e}")


def test_table_creation():
    """Test that tables can be created in PostgreSQL"""
    try:
        # This will try to create tables if they don't exist
        from src.database.connection import create_db_and_tables
        create_db_and_tables()

        # If we get here without exception, table creation worked
        assert True
    except Exception as e:
        pytest.fail(f"Failed to create tables: {e}")