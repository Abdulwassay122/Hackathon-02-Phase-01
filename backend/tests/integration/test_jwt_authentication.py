import pytest
import os
from fastapi.testclient import TestClient
from src.main import app
from src.config import settings

def test_database_environment_variable():
    """Test that the database URL is properly set to PostgreSQL"""
    assert settings.database_url is not None
    assert "postgresql" in settings.database_url.lower(), f"Expected PostgreSQL URL, got: {settings.database_url}"

def test_better_auth_secret_exists():
    """Test that the better auth secret is configured"""
    assert settings.better_auth_secret is not None, "BETTER_AUTH_SECRET should be set in environment"

def test_app_startup():
    """Test that the app starts up without errors"""
    client = TestClient(app)

    # This test mainly verifies that the startup event handler runs without errors
    # If there were issues with the database connection, the app would fail to start
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()