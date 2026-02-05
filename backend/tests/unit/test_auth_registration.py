import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.models.user import User
from src.database.connection import engine


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session
        # Clean up after test
        session.rollback()


def test_register_endpoint_valid_data(client, db_session):
    """Test successful registration with valid data."""
    # Clear any existing users with test credentials
    existing_user = db_session.exec(select(User).where(User.username == "testuser")).first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    existing_email = db_session.exec(select(User).where(User.email == "test@example.com")).first()
    if existing_email:
        db_session.delete(existing_email)
        db_session.commit()

    # Register a new user
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    # Assert the response
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["is_active"] is True

    # Verify the user was created in the database
    created_user = db_session.exec(select(User).where(User.username == "testuser")).first()
    assert created_user is not None
    assert created_user.email == "test@example.com"


def test_register_duplicate_username(client, db_session):
    """Test registration with duplicate username."""
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "username": "uniqueuser",
            "email": "unique@example.com",
            "password": "SecurePass123!"
        }
    )

    # Try to register with the same username
    response = client.post(
        "/auth/register",
        json={
            "username": "uniqueuser",
            "email": "different@example.com",
            "password": "SecurePass123!"
        }
    )

    # Should return 409 Conflict
    assert response.status_code == 409
    data = response.json()
    assert "Username already exists" in data["detail"]


def test_register_duplicate_email(client, db_session):
    """Test registration with duplicate email."""
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "username": "firstuser",
            "email": "same@example.com",
            "password": "SecurePass123!"
        }
    )

    # Try to register with the same email
    response = client.post(
        "/auth/register",
        json={
            "username": "seconduser",
            "email": "same@example.com",
            "password": "SecurePass123!"
        }
    )

    # Should return 409 Conflict
    assert response.status_code == 409
    data = response.json()
    assert "Email already exists" in data["detail"]


def test_register_invalid_data(client, db_session):
    """Test registration with invalid data."""
    # Test with short password
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "short"  # Less than 8 characters
        }
    )

    # Should return 422 Unprocessable Entity
    assert response.status_code in [422, 400]  # Both are acceptable for validation errors

    # Test with invalid email format
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "SecurePass123!"
        }
    )

    # Should return 422 Unprocessable Entity
    assert response.status_code in [422, 400]


def test_register_special_characters_handling(client, db_session):
    """Test registration with special characters and potential injection attempts."""
    # Test with special characters in username and email
    response = client.post(
        "/auth/register",
        json={
            "username": "user_with_special_chars_123",
            "email": "user.special+tag@example-domain.com",
            "password": "SecurePass123!"
        }
    )

    # Should succeed
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == "user_with_special_chars_123"
    assert data["user"]["email"] == "user.special+tag@example-domain.com"

    # Clean up
    created_user = db_session.exec(select(User).where(User.username == "user_with_special_chars_123")).first()
    if created_user:
        db_session.delete(created_user)
        db_session.commit()


def test_register_sql_injection_protection(client, db_session):
    """Test that the registration endpoint is protected against SQL injection."""
    # Test with potential SQL injection in username
    response = client.post(
        "/auth/register",
        json={
            "username": "'; DROP TABLE users; --",
            "email": "safe@example.com",
            "password": "SecurePass123!"
        }
    )

    # Should return 422 or 400 due to validation, not crash
    assert response.status_code in [201, 400, 422]

    # If it succeeded, verify the malicious input was sanitized
    if response.status_code == 201:
        data = response.json()
        # The malicious input should either be rejected by validation
        # or properly escaped by the ORM
        assert "'; DROP TABLE users; --" != data["user"]["username"]

        # Clean up if user was created
        created_user = db_session.exec(select(User).where(User.username == "'; DROP TABLE users; --")).first()
        if created_user:
            db_session.delete(created_user)
            db_session.commit()