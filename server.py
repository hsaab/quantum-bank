from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from api.hello import handle_hello
from api.home import handle_home
from api.time import handle_time
from api.echo import handle_echo
from api.about import handle_about
from api.four_o_four import handle_404

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == "/":
            handle_home(self)
        elif path == "/hello":
            handle_hello(self)
        elif path == "/time":
            handle_time(self)
        elif path == "/about":
            handle_about(self)
        else:
            handle_404(self)

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
