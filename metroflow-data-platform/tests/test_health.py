from fastapi.testclient import TestClient
from ingestion.main import app



client = TestClient(app)

def test_health_endpoint_returns_200():

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status" : "healthy"}