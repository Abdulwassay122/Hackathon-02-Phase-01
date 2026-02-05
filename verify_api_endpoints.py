#!/usr/bin/env python3
"""
Simple verification script to test the registration API endpoint
"""
import requests
import json
import sys
import time

def test_registration_endpoint():
    """
    Test the registration endpoint with valid data
    """
    print("Testing registration endpoint...")

    # Base URL for the API
    base_url = "http://localhost:8000"

    # Test data for registration
    test_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"testuser_{int(time.time())}@example.com",
        "password": "SecurePassword123!"
    }

    try:
        # Make a POST request to the register endpoint
        response = requests.post(f"{base_url}/auth/register", json=test_data)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("[SUCCESS] Registration endpoint test PASSED")
            response_data = response.json()

            # Check if we got a proper token response
            if "access_token" in response_data and "token_type" in response_data:
                print("[SUCCESS] Token received successfully")
                return True
            else:
                print("[ERROR] Expected token in response but didn't get it")
                return False
        elif response.status_code == 409:
            print("[WARNING] User already exists (expected if running multiple times)")
            return True  # This is still a valid response
        else:
            print(f"[ERROR] Registration endpoint test FAILED with status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Is the backend running on http://localhost:8000?")
        print("Please start the backend server with: cd backend && uvicorn src.main:app --reload")
        return False
    except Exception as e:
        print(f"[ERROR] Error during registration test: {str(e)}")
        return False

def test_duplicate_registration():
    """
    Test duplicate registration prevention
    """
    print("\nTesting duplicate registration prevention...")

    base_url = "http://localhost:8000"

    # Same test data for duplicate attempt
    test_data = {
        "username": "duplicate_test_user",
        "email": "duplicate_test@example.com",
        "password": "SecurePassword123!"
    }

    try:
        # First registration should succeed
        response1 = requests.post(f"{base_url}/auth/register", json=test_data)
        print(f"First registration - Status: {response1.status_code}")

        if response1.status_code in [201, 409]:  # 201 for new user, 409 if already exists
            # Second registration with same data should fail
            response2 = requests.post(f"{base_url}/auth/register", json=test_data)
            print(f"Duplicate registration - Status: {response2.status_code}")

            if response2.status_code == 409:
                print("[SUCCESS] Duplicate registration prevention test PASSED")
                return True
            else:
                print("[ERROR] Duplicate registration should return 409 Conflict")
                return False
        else:
            print(f"[ERROR] First registration failed unexpectedly with status {response1.status_code}")
            return False

    except Exception as e:
        print(f"[ERROR] Error during duplicate registration test: {str(e)}")
        return False

def test_invalid_data_validation():
    """
    Test validation with invalid data
    """
    print("\nTesting validation with invalid data...")

    base_url = "http://localhost:8000"

    # Test data with invalid email
    invalid_data = {
        "username": "testuser_invalid",
        "email": "not_an_email",  # Invalid email format
        "password": "short"       # Too short password
    }

    try:
        response = requests.post(f"{base_url}/auth/register", json=invalid_data)
        print(f"Invalid data registration - Status: {response.status_code}")

        # Should return either 422 (validation error) or 400 (bad request)
        if response.status_code in [400, 422]:
            print("[SUCCESS] Invalid data validation test PASSED")
            return True
        else:
            print(f"[ERROR] Invalid data should return 400/422, got {response.status_code}")
            return False

    except Exception as e:
        print(f"[ERROR] Error during invalid data test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting API endpoint verification tests...\n")

    # Run all tests
    test1_passed = test_registration_endpoint()
    test2_passed = test_duplicate_registration()
    test3_passed = test_invalid_data_validation()

    print(f"\n--- Test Results ---")
    print(f"Registration endpoint test: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"Duplicate registration test: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"Invalid data validation test: {'PASSED' if test3_passed else 'FAILED'}")

    all_passed = test1_passed and test2_passed and test3_passed

    if all_passed:
        print("\n[SUCCESS] All tests PASSED!")
        sys.exit(0)
    else:
        print("\n[ERROR] Some tests FAILED!")
        sys.exit(1)