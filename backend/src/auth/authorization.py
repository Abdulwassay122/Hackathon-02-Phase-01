from fastapi import HTTPException
from typing import Any

def check_user_owns_resource(user_id: int, resource_user_id: int) -> bool:
    """
    Check if the authenticated user owns the resource
    """
    return str(user_id) == str(resource_user_id)

def require_user_ownership(user_id: int, resource_user_id: int, resource_type: str = "resource"):
    """
    Raise an HTTPException if the user doesn't own the resource
    """
    if not check_user_owns_resource(user_id, resource_user_id):
        raise HTTPException(
            status_code=403,
            detail=f"Not authorized to access this {resource_type}"
        )