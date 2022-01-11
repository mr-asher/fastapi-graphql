import json
from fastapi.testclient import TestClient

def test_health_check(client: TestClient) -> None:
    data = { 
        "query":  """
            {
                healthCheck {
                    ok
                }
            }
        """
    }
    
    r = client.post("/graphql", json=data)
    print(r.__dict__)
    print(r.content)
    print(r.content.decode("UTF-8"))
    data = json.loads(r.content.decode("UTF-8"))
    assert 200 <= r.status_code < 300
    assert "errors" not in data
    assert data["data"]["healthCheck"]

