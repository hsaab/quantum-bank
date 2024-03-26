import unittest
import http.client

class TestHTTPServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = http.client.HTTPConnection("localhost", 8000)

    def test_home_page(self):
        self.conn.request("GET", "/")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("Welcome to the Home Page", response.read().decode())

    def test_hello_page(self):
        self.conn.request("GET", "/hello")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("Hello, Worl", response.read().decode())

    def test_time_page(self):
        self.conn.request("GET", "/time")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        # This test assumes the response includes a timestamp in the format 'YYYY-MM-DD HH:MM:SS'
        self.assertRegex(response.read().decode(), r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    def test_echo_with_message(self):
        self.conn.request("GET", "/*?msg=HelloTest")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("Echo: HelloTest", response.read().decode())

    def test_echo_empty_message(self):
        self.conn.request("GET", "/echo")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("Echo: ", response.read().decode())

    def test_about_page(self):
        self.conn.request("GET", "/about")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("This is a simple HTTP server", response.read().decode())

    def test_404_page(self):
        self.conn.request("GET", "/nonexistent")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 404)
        self.assertIn("404 Not Found", response.read().decode())

    def test_echo_with_special_characters(self):
        self.conn.request("GET", "/echo?msg=%40%23%24%25%5E")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn("Echo: @#$%^", response.read().decode())

    def test_multiple_echo_messages(self):
        messages = ["Test1", "Test2"]
        for msg in messages:
            with self.subTest(msg=msg):
                self.conn.request("GET", f"/echo?msg={msg}")
                response = self.conn.getresponse()
                self.assertEqual(response.status, 200)
                self.assertIn(f"Echo: {msg}", response.read().decode())

    def test_home_page_method_not_allowed(self):
        self.conn.request("POST", "/")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 501)  # Assuming server is updated to handle method not allowed

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

if __name__ == '__main__':
    unittest.main()
