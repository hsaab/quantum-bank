import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_hello(client):
    response = client.get('/hello')
    assert b"Hello, World!" in response.data

