from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

# Can't get this to work in time - getting "No module named 'httpx', probably just need to add to pyproject.toml

client = TestClient(app)

def test_get_user():
    response = client.get('/users/me')
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Alice"}


