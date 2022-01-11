from app.tests.utils.utils import execute_query
from fastapi.testclient import TestClient

def test_health_check(client: TestClient) -> None:
    query = """
            query {
                healthCheck {
                    ok
                }
            }
        """
    
    data = execute_query(client, query)
    assert "errors" not in data
    assert data["data"]["healthCheck"]
