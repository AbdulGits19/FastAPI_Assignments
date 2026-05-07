import pytest
from fastapi.testclient import TestClient
from Backend.app.main import app

client = TestClient(app)

def test_read_main():
    """Test the public root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Hospital Management System API"}

def test_get_doctors_pagination():
    """Test that pagination logic is working"""
    response = client.get("/doctors/?limit=5")
    assert response.status_code == 200
    # Check if the standardized response structure is there
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert len(data["data"]) <= 5

def test_unauthorized_admin_route():
    """Test that RBAC/Auth is protecting routes"""
    # Trying to access admin-only or protected route without a token
    response = client.get("/appointments/")
    # If your route is protected, it should return 401
    assert response.status_code == 401