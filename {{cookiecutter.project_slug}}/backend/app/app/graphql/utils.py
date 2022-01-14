from typing import Any 
from sqlalchemy.orm import Session

def get_context_db(info: Any) -> Session:
    """Helper function to get the db from the info context."""
    return info.context["request"]["state"]["db"]
