import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_about_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_about(client):
    response = client.get('/about')
    assert b"This is a simple HTTP server." in response.data

