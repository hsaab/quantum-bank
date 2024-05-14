import pytest
from api.time import handle_time
from test.server_mock import Mock_Server

@pytest.fixture(scope="module")
def mock_server_instance():
    return Mock_Server()

def test_handle_time(mock_server_instance):
    handle_time(mock_server_instance)
    
    assert mock_server_instance.response == 200
    assert mock_server_instance.header == ('Content-type', 'text/html')