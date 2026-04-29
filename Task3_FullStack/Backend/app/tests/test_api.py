from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_login_and_access_protected_route():
    # 1. Register a test user
    client.post("/auth/register", json={"username": "testuser", "password": "password123"})
    
    # 2. Login to get token
    login_response = client.post("/auth/login", data={"username": "testuser", "password": "password123"})
    token = login_response.json()["access_token"]
    
    # 3. Use token to hit a locked route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/doctors/", headers=headers)
    assert response.status_code == 200