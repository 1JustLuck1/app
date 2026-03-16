# tests/test_simple.py

def test_health_endpoint():
    """Минимальный тест — только статус код"""
    from fastapi.testclient import TestClient
    from main import app
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200  # ✅ Всё!