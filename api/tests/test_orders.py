from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    # Mock database session to avoid touching real data
    return mocker.Mock()


# Test that the app starts and serves documentation
def test_app_starts():
    response = client.get("/docs")
    assert response.status_code == 200



# Test retrieving all orders from the controller
def test_get_orders(db_session):
    # Setup mock orders to return
    fake_orders = [
        model.Order(id=1, guest_name="Jake", status="Received"),
        model.Order(id=2, guest_name="Sage", status="In Progress")
    ]

    db_session.query().all.return_value = fake_orders

    # Retrieve orders from controller
    retrieved_orders = controller.read_all(db_session)
    
    # Verify the controller retrieved the correct data
    assert retrieved_orders is not None
    assert len(retrieved_orders) == 2
    assert retrieved_orders[0].guest_name == "Jake"
    assert retrieved_orders[1].status == "In Progress"