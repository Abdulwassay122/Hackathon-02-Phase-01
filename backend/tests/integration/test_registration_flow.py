import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.auth_response import TokenResponse
from src.services.auth_service import AuthService
from sqlmodel import Session, select
from src.database.connection import engine
from src.models.user import User


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


def test_complete_registration_flow_integration(client):
    """Test the complete registration flow from API to database."""

    # Register a new user
    response = client.post(
        "/auth/register",
        json={
            "username": "integration_user",
            "email": "integration@test.com",
            "password": "SecurePass123!"
        }
    )

    # Verify the response
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["username"] == "integration_user"
    assert data["user"]["email"] == "integration@test.com"
    assert data["user"]["is_active"] is True

    # Verify the user exists in the database
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == "integration_user")).first()
        assert user is not None
        assert user.email == "integration@test.com"
        assert user.is_active is True
        # Verify password was hashed (not stored in plain text)
        assert user.password_hash != "SecurePass123!"

        # Test that the user can be authenticated after registration
        token_response = AuthService.authenticate_user(session, "integration_user", "SecurePass123!")
        assert token_response is not None
        assert isinstance(token_response, TokenResponse)
        assert token_response.token_type == "bearer"

        # Clean up: remove test user
        session.delete(user)
        session.commit()


def test_error_scenarios_integration(client):
    """Test error scenarios in the registration flow."""

    # Test invalid email format
    response = client.post(
        "/auth/register",
        json={
            "username": "validuser",
            "email": "invalid-email-format",
            "password": "SecurePass123!"
        }
    )
    assert response.status_code in [400, 422]

    # Test short password
    response = client.post(
        "/auth/register",
        json={
            "username": "validuser",
            "email": "valid@example.com",
            "password": "short"
        }
    )
    assert response.status_code in [400, 422]

    # Test missing required fields
    response = client.post(
        "/auth/register",
        json={
            "username": "validuser",
            "email": "valid@example.com"
            # Missing password field
        }
    )
    assert response.status_code in [400, 422]


def test_security_measures_verification(client):
    """Verify security measures like password hashing."""

    # Register a user
    response = client.post(
        "/auth/register",
        json={
            "username": "security_test",
            "email": "security@test.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 201

    # Check that the password was properly hashed in the database
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == "security_test")).first()
        assert user is not None
        # The password should not be stored in plain text
        assert user.password_hash != "SecurePass123!"

        # Verify that the stored hash can be used for authentication
        auth_result = AuthService.authenticate_user(session, "security_test", "SecurePass123!")
        assert auth_result is not None

        # Verify that wrong password fails authentication
        wrong_auth_result = AuthService.authenticate_user(session, "security_test", "WrongPassword123!")
        assert wrong_auth_result is None

        # Clean up
        session.delete(user)
        session.commit()