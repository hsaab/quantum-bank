from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == "/":
            self.handle_home()
        elif path == "/hello":
            self.handle_hello()
        elif path == "/time":
            self.handle_time()
        elif path == "/echo":
            self.handle_echo(query_params)
        elif path == "/about":
            self.handle_about()
        else:
            self.handle_404()

    def handle_home(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Welcome to the Home Page!")

    def handle_hello(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # yo
        self.wfile.write(b"Hello, World!")

    def handle_time(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.wfile.write(f"Current server time is: {current_time}".encode())

    def handle_echo(self, query_params):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = query_params.get('msg', [''])[0]  # Default to empty string if not provided
        print(message)
        self.wfile.write(f"Echo: {message}".encode())

    def handle_about(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"This is a simple HTTP server.")

    def handle_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
