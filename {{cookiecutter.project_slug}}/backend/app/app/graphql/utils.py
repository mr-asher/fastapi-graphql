from typing import Any 
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

def get_context_db(info: Any) -> Session:
    """Helper function to get the db from the info context."""
    return info.context["request"]["state"]["db"]

def get_authorize(info: Any) -> AuthJWT:
    return info.context["request"]["state"]["authorize"]
