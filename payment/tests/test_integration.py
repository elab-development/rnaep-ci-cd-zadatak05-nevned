import pytest
import os
from redis_om import get_redis_connection
from main import Order

@pytest.fixture(scope="module")
def redis_conn():
    """Povezivanje na testni Redis"""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    conn = get_redis_connection(host=host, port=port, decode_responses=True)
    return conn

def test_redis_order_integration(redis_conn):
    """Integracioni test: Provera direktnog upisa i čitanja iz Redis DB"""
    Order.Meta.database = redis_conn
    
    order = Order(
        product_id="test_integration_id",
        price=50.0,
        fee=10.0,
        total=60.0,
        quantity=1,
        status="completed"
    )
    saved_order = order.save()
    
    
    fetched_order = Order.get(saved_order.pk)
    
    assert fetched_order.product_id == "test_integration_id"
    assert fetched_order.total == 60.0
    assert fetched_order.status == "completed"
    
    Order.delete(saved_order.pk)