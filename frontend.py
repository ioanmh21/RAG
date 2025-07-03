import http.server
import socketserver
import os

PORT = 8001 # Folosește un port diferit de cel al backend-ului FastAPI (ex: 8000)

WEB_DIR = os.path.dirname(os.path.abspath(__file__)) # Directorul unde se află acest script

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    # Suprascrie logica pentru a servi index.html dacă se accesează rădăcina
    def do_GET(self):
        if self.path == '/':
            self.path = '/interface.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Serving files from: {WEB_DIR}")
print(f"Frontend server running on http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()

