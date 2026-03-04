"""Serve AegisLab Dashboard over HTTP so API calls work (avoids file:// CORS issues)."""
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8502
DIR = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://127.0.0.1:{PORT}/aegislab-dashboard.html"
    print("=" * 50)
    print("AegisLab Dashboard")
    print("=" * 50)
    print(f"Open: {url}")
    print("Press Ctrl+C to stop.")
    print("=" * 50)
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
