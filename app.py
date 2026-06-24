import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.getenv("APP_VERSION", "unknown")
PORT = int(os.getenv("PORT", 8080))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"version: {VERSION}\n".encode())

    def log_message(self, format, *args):
        pass  # suprimir logs de acceso


if __name__ == "__main__":
    print(f"Servidor iniciado en puerto {PORT}, version={VERSION}")
    HTTPServer(("", PORT), Handler).serve_forever()
