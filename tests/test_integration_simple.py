"""Simple integration tests for HiveBox API - 3 approaches"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import httpx
import requests
from fastapi.testclient import TestClient
from src.main import app

class TestWithFastAPIClient:
    """Approach 1: FastAPI TestClient"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_all_endpoints(self):
        """Test all endpoints exist and return 200"""
        endpoints = ["/", "/version", "/health", "/readyz", "/metrics"]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200
            print(f"✅ {endpoint}: {response.status_code}")

    def test_temperature_endpoint(self):
        """Test temperature endpoint returns status field"""
        response = self.client.get("/temperature")
        assert response.status_code == 200
        data = response.json()
        
        # Should have status field now
        if "error" not in data:
            assert "status" in data
            assert data["status"] in ["Too Cold", "Good", "Too Hot"]

class TestWithHttpx:
    """Approach 2: httpx AsyncClient"""
    
    @pytest.mark.asyncio
    async def test_async_requests(self):
        """Test endpoints asynchronously"""
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")
            assert response.status_code == 200
            
            response = await client.get("/metrics")
            assert response.status_code == 200
            assert "python_info" in response.text or "http_requests" in response.text

class TestWithRequests:
    """Approach 3: requests (requires running server)"""
    
    @pytest.mark.skipif(True, reason="Enable manually for live server testing")
    def test_live_server(self):
        """Test against live server at localhost:8000"""
        base_url = "http://localhost:8000"
        
        response = requests.get(f"{base_url}/readyz")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
