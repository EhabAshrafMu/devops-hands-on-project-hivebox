import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "HiveBox" in data["message"]

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.0.1"
    assert data["name"] == "HiveBox"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_temperature_endpoint():
    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.json()
    assert "average_temperature" in data
    # Either we get a number or None (if no data available)
    if data["average_temperature"] is not None:
        assert isinstance(data["average_temperature"], (int, float))
        assert "sensor_count" in data