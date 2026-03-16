# app/tests/test_simple.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_returns_200():
    """Тест: главная страница возвращает статус 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]