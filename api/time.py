from datetime import datetime

def handle_time(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.wfile.write(f"Current server time is: {current_time}".encode())