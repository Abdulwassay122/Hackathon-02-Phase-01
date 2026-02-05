#!/usr/bin/env python3
"""
Initialize the database and test the registration endpoint
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from backend.src.database.connection import create_db_and_tables
from backend.src.main import app
from fastapi.testclient import TestClient

def initialize_database():
    """Initialize the database by calling create_db_and_tables"""
    print("Initializing database...")
    create_db_and_tables()
    print("Database initialized successfully!")

def test_registration():
    """Test registration after initializing the database"""
    # Initialize the database first
    initialize_database()

    # Create test client
    client = TestClient(app)

    # Test data for registration
    test_data = {
        "username": "testuser_init",
        "email": "testuser_init@example.com",
        "password": "SecurePassword123!"
    }

    try:
        print("Making registration request...")
        response = client.post("/auth/register", json=test_data)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("[SUCCESS] Registration successful!")
            return True
        elif response.status_code == 409:
            print("[WARNING] User already exists (acceptable)")
            return True
        else:
            print(f"[ERROR] Registration failed with status {response.status_code}")

            # Try to get more detailed error info
            try:
                error_detail = response.json()
                print(f"Detailed error: {error_detail}")
            except:
                print("Could not parse error response as JSON")

            return False

    except Exception as e:
        print(f"[ERROR] Exception during registration test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing registration endpoint after database initialization...")
    success = test_registration()

    if success:
        print("\n[SUCCESS] Test passed!")
        sys.exit(0)
    else:
        print("\n[ERROR] Test failed!")
        sys.exit(1)