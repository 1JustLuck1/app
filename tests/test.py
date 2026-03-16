# app/tests/test_simple.py
from fastapi.testclient import TestClient
from app.main import app

# Создаём тестовый клиент
client = TestClient(app)

def test_root_returns_200():
    """Тест: главная страница возвращает статус 200"""
    response = client.get("/")
    
    # Проверяем статус код
    assert response.status_code == 200
    
    # Проверяем, что это HTML
    assert "text/html" in response.headers["content-type"]
    
    # Проверяем, что в ответе есть HTML-тег
    assert "<html" in response.text.lower()