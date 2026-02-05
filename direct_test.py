#!/usr/bin/env python3
"""
Direct test of the registration endpoint to identify the issue
"""
import sys
import os
import asyncio
import traceback

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from fastapi.testclient import TestClient
from backend.src.main import app

def test_registration_direct():
    """Test registration using FastAPI TestClient"""
    client = TestClient(app)

    # Test data for registration
    test_data = {
        "username": "testuser_direct",
        "email": "testuser_direct@example.com",
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
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing registration endpoint directly with TestClient...")
    success = test_registration_direct()

    if success:
        print("\n[SUCCESS] Test passed!")
        sys.exit(0)
    else:
        print("\n[ERROR] Test failed!")
        sys.exit(1)