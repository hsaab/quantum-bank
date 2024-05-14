import pytest
from api.four_o_four import handle_404
from test.server_mock import Mock_Server

@pytest.fixture(scope="module")
def mock_server_instance():
    return Mock_Server()

def test_404(mock_server_instance):
    handle_404(mock_server_instance)
    
    assert mock_server_instance.response == 404
    assert mock_server_instance.header == ('Content-type', 'text/html')
    assert mock_server_instance.message == b"404 Not Found"

