class Mock_Server():
    def __init__(self):
        print("init Mock Server")
        self.wfile = self.wfileClass(self)

    def send_response(self, response):
        self.response = response
    
    def send_header(self, header1, header2):
        self.header = header1,header2
    
    def end_headers(self):
        print("yo")
    
    class wfileClass:
        def __init__(self, parent_instance):
            self.parent = parent_instance

        def write(self, message):
            self.parent.message = message