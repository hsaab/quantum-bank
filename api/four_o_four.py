def handle_404(self):
    self.send_response(404)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write(b"404 Not Found")