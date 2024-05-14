import pytest
from api.home import handle_home
from test.server_mock import Mock_Server

@pytest.fixture(scope="module")
def mock_server_instance():
    return Mock_Server()

def test_home_page(mock_server_instance):
    handle_home(mock_server_instance)
    
    assert mock_server_instance.response == 200
    assert mock_server_instance.header == ('Content-type', 'text/html')
    assert mock_server_instance.message == b"Welcome to the Home Page!"

