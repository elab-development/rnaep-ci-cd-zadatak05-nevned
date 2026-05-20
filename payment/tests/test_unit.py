import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


with patch('database.redis') as mock_redis:
    from main import app, Order

client = TestClient(app)

@pytest.mark.asyncio
@patch('httpx.AsyncClient.get')
@patch.object(Order, 'save', return_value=None)
async def test_create_order_unit(mock_save, mock_get):
    """Unit test: Testira kreiranje porudžbine uz mokovanje eksternog HTTP poziva"""
    
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "prod_123", "name": "Test Product", "price": 100.0, "quantity": 10}
    mock_get.return_value = mock_response

    payload = {"id": "prod_123", "quantity": 2}
    
    
    with patch('fastapi.BackgroundTasks.add_task') as mock_bg:
        response = client.post("/orders", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "prod_123"
        assert data["price"] == 100.0
        assert data["fee"] == 20.0  # 0.2 * 100
        assert data["total"] == 240.0  # 1.2 * 100 * 2
        assert data["status"] == "pending"