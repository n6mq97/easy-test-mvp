import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_read_main(client):
    """Тест основного эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check(client):
    """Тест эндпоинта проверки здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
