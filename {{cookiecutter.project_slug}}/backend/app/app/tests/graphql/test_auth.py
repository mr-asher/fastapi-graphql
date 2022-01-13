from app.tests.utils.utils import execute_query
from fastapi.testclient import TestClient

from app.core.config import settings

def test_token_auth(client: TestClient) -> None:
    mutation = f"""
        mutation {{
            tokenAuth(username: "{settings.FIRST_SUPERUSER}", password: "{settings.FIRST_SUPERUSER_PASSWORD}") {{
                token
            }}
        }}
    """
    data = execute_query(client, mutation)
    assert "errors" not in data
    assert data["data"]["tokenAuth"]["token"]

