import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from my_app import app  # Import your FastAPI app here
from my_app.models import Car  # Import your Car model here

client = TestClient(app)

# Helper function to create a mock database session
def mock_db_session():
    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    return mock_session

# Test Create Car
@patch('my_app.dependencies.get_db')  # Replace 'my_app.dependencies' with the actual path to your dependency
def test_create_car(mock_get_db):
    mock_db = mock_db_session()
    mock_get_db.return_value = mock_db

    response = client.post("/cars/", json={"make": "Toyota", "model": "Corolla", "year": 2020})
    assert response.status_code == 201
    assert response.json() == {"make": "Toyota", "model": "Corolla", "year": 2020}

# Test Retrieve All Cars
@patch('my_app.dependencies.get_db')
def test_retrieve_all_cars(mock_get_db):
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = [
        Car(make="Toyota", model="Corolla", year=2020),
        Car(make="Honda", model="Civic", year=2021)
    ]
    mock_get_db.return_value = mock_db

    response = client.get("/cars/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0] == {"make": "Toyota", "model": "Corolla", "year": 2020}
    assert response.json()[1] == {"make": "Honda", "model": "Civic", "year": 2021}

# Test Retrieve Specific Car
@patch('my_app.dependencies.get_db')
def test_retrieve_specific_car(mock_get_db):
    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = Car(make="Toyota", model="Corolla", year=2020)
    mock_get_db.return_value = mock_db

    response = client.get("/cars/1")
    assert response.status_code == 200
    assert response.json() == {"make": "Toyota", "model": "Corolla", "year": 2020}

# Test Update Car
@patch('my_app.dependencies.get_db')
def test_update_car(mock_get_db):
    mock_db = mock_db_session()
    mock_get_db.return_value = mock_db

    response = client.put("/cars/1", json={"make": "Toyota", "model": "Camry", "year": 2021})
    assert response.status_code == 200
    assert response.json() == {"make": "Toyota", "model": "Camry", "year": 2021}

# Test Delete Car
@patch('my_app.dependencies.get_db')
def test_delete_car(mock_get_db):
    mock_db = mock_db_session()
    mock_get_db.return_value = mock_db

    response = client.delete("/cars/1")
    assert response.status_code == 204
    assert response.text == ""

# Invalid case: Missing required fields
@patch('my_app.dependencies.get_db')
def test_create_car_invalid_data(mock_get_db):
    response = client.post("/cars/", json={"make": "Toyota"})  # Missing model and year
    assert response.status_code == 422

# Invalid case: Car not found
@patch('my_app.dependencies.get_db')
def test_retrieve_non_existent_car(mock_get_db):
    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    mock_get_db.return_value = mock_db

    response = client.get("/cars/999")
    assert response.status_code == 404

# Invalid case: Update non-existent car
@patch('my_app.dependencies.get_db')
def test_update_non_existent_car(mock_get_db):
    mock_db = mock_db_session()
    mock_get_db.return_value = mock_db

    response = client.put("/cars/999", json={"make": "Toyota", "model": "Camry", "year": 2021})
    assert response.status_code == 404

# Invalid case: Delete non-existent car
@patch('my_app.dependencies.get_db')
def test_delete_non_existent_car(mock_get_db):
    mock_db = mock_db_session()
    mock_get_db.return_value = mock_db

    response = client.delete("/cars/999")
    assert response.status_code == 404

