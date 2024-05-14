import re
import pytest
import http.client

@pytest.fixture(scope="module")
def conn():
    connection = http.client.HTTPConnection("localhost", 8000)
    yield connection
    connection.close()

def test_home_page(conn):
    conn.request("GET", "/")
    response = conn.getresponse()
    assert response.status == 200
    assert "Welcome to the Home Page" in response.read().decode()

def test_hello_page(conn):
    conn.request("GET", "/hello")
    response = conn.getresponse()
    assert response.status == 200
    assert "Hello, World!" in response.read().decode()

def test_time_page(conn):
    conn.request("GET", "/time")
    response = conn.getresponse()
    assert response.status == 200
    # This test assumes the response includes a timestamp in the format 'YYYY-MM-DD HH:MM:SS'
    assert re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', response.read().decode())

def test_echo_with_message(conn):
    conn.request("GET", "/echo?msg=HelloTest")
    response = conn.getresponse()
    assert response.status == 200
    assert "Echo: HelloTest" in response.read().decode()

def test_echo_empty_message(conn):
    conn.request("GET", "/echo")
    response = conn.getresponse()
    assert response.status == 200
    assert "Echo: " in response.read().decode()

def test_about_page(conn):
    conn.request("GET", "/about")
    response = conn.getresponse()
    assert response.status == 200
    assert "This is a simple HTTP server" in response.read().decode()

def test_404_page(conn):
    conn.request("GET", "/nonexistent")
    response = conn.getresponse()
    assert response.status == 404
    assert "404 Not Found" in response.read().decode()

def test_echo_with_special_characters(conn):
    conn.request("GET", "/echo?msg=%40%23%24%25%5E")
    response = conn.getresponse()
    assert response.status == 200
    assert "Echo: @#$%^" in response.read().decode()

@pytest.mark.parametrize("msg", ["Test1", "Test2"])
def test_multiple_echo_messages(conn, msg):
    conn.request("GET", f"/echo?msg={msg}")
    response = conn.getresponse()
    assert response.status == 200
    assert f"Echo: {msg}" in response.read().decode()

def test_home_page_method_not_allowed(conn):
    conn.request("POST", "/")
    response = conn.getresponse()
    assert response.status == 501  # Assuming server is updated to handle method not allowed
