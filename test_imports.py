import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Import and test the auth module directly
try:
    from backend.src.api.auth import router
    print("Auth router imported successfully")
except Exception as e:
    print(f"Error importing auth router: {e}")
    import traceback
    traceback.print_exc()

# Test the individual components
try:
    from backend.src.services.auth_service import AuthService
    print("AuthService imported successfully")
except Exception as e:
    print(f"Error importing AuthService: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.models.auth_response import RegisterRequest
    print("RegisterRequest imported successfully")

    # Test the model
    test_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    req = RegisterRequest(**test_data)
    print(f"RegisterRequest validation passed: {req.username}")
except Exception as e:
    print(f"Error with RegisterRequest: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.models.user import User
    print("User model imported successfully")
except Exception as e:
    print(f"Error importing User model: {e}")
    import traceback
    traceback.print_exc()