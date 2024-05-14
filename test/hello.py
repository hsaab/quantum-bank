import pytest
from api.hello import handle_hello
from test.server_mock import Mock_Server

@pytest.fixture(scope="module")
def mock_server_instance():
    return Mock_Server()

def test_hello(mock_server_instance):
    handle_hello(mock_server_instance)
    
    assert mock_server_instance.response == 200
    assert mock_server_instance.header == ('Content-type', 'text/html')
    assert mock_server_instance.message == b"Hello, World!"