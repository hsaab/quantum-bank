import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_404_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_404(client):
    response = client.get('/yodawg20044')
    assert b"404 Not Found" in response.data

