import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_non_existent_order():
    """Funkcionalni test: Provera ponašanja celokupnog API-ja za 404 grešku"""
    response = client.get("/orders/ne-postoji-ovaj-id")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found" or "Order not found" in response.json()["detail"]