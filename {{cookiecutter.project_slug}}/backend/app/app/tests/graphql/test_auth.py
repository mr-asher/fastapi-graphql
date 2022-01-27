from typing import Dict
from app.tests.utils.utils import execute_query
from fastapi.testclient import TestClient

from app.core.config import settings


def test_token_auth(client: TestClient) -> None:
    mutation = f"""
        mutation {{
            tokenAuth(
                input: {{ 
                    username: "{settings.FIRST_SUPERUSER}", 
                    password: "{settings.FIRST_SUPERUSER_PASSWORD}" 
                }}
            ) {{
                token
            }}
        }}
    """
    data = execute_query(client, mutation)
    assert "errors" not in data
    assert data["data"]["tokenAuth"]["token"]

def test_use_access_token(client: TestClient, superuser_token_headers: Dict[str, str]) -> None:
    query = """
        query {
            checkAuthToken {
                ok
            }
        }
    """
    data = execute_query(client, query, headers=superuser_token_headers)
    assert "errors" not in data
    assert data["data"]["checkAuthToken"]

def test_use_access_token_without_token(client: TestClient) -> None:
    query = """
        query {
            checkAuthToken {
                ok
            }
        }
    """
    data = execute_query(client, query)
    assert "errors" in data
    assert not data["data"]["checkAuthToken"]
