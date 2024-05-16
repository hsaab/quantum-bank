import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_time_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_time(client):
    response = client.get('/time')
    print(response.data)
    assert b"Current server time is:" in response.data

