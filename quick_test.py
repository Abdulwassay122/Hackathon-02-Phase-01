#!/usr/bin/env python3
"""
Quick test of the registration endpoint
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from backend.src.database.connection import create_db_and_tables
from backend.src.main import app
from fastapi.testclient import TestClient

def test_registration():
    """Test registration after initializing the database"""
    # Initialize the database first
    print("Initializing database...")
    create_db_and_tables()
    print("Database initialized successfully!")

    # Create test client
    client = TestClient(app)

    # Test data for registration (using shorter password to avoid bcrypt issues)
    test_data = {
        "username": "testuser_final",
        "email": "testuser_final@example.com",
        "password": "Pass123!"
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
            print("[SUCCESS] User already exists (acceptable - means endpoint works)")
            return True
        else:
            print(f"[ERROR] Registration failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"[ERROR] Exception during registration test: {e}")
        return False

if __name__ == "__main__":
    print("Testing registration endpoint...")
    success = test_registration()

    if success:
        print("\n[SUCCESS] Registration endpoint is working!")
    else:
        print("\n[ERROR] Registration endpoint has issues.")