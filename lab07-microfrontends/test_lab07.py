import pytest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_api_v1_exists():
    response = client.get("/api/v1/catalogo")
    assert response.status_code == 200
def test_bff_endpoint_exists():
    response = client.get("/api/bff/home")
    assert response.status_code == 200
def test_static_files_loading():
    assert client.get("/").status_code == 200
    assert client.get("/static/catalogo.js").status_code == 200
