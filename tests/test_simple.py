
def test_health_endpoint():
    """Проверяем, что эндпоинт здоровья возвращает 200"""
    # Импортируем только то, что нужно для теста
    from fastapi.testclient import TestClient
    from main import app  # ← импортируем app
    
    client = TestClient(app)
    response = client.get("/health")  # или "/"
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}  # или ожидаемый ответ