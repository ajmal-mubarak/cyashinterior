import os, sys, http.server, socketserver

PORT = 3000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public_html')

class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Strip query string for path check
        path = self.path.split('?')[0].rstrip('/')
        full_path = os.path.join(DIRECTORY, path.lstrip('/'))

        # If requesting clean URL without .html and .html exists, rewrite
        if path and not os.path.isdir(full_path) and not os.path.exists(full_path):
            if os.path.exists(full_path + '.html'):
                self.path = path + '.html'
            elif os.path.exists(os.path.join(full_path, 'index.html')):
                self.path = path + '/index.html'

        return super().do_GET()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanUrlHandler) as httpd:
        print(f"Serving Cyash Contracting website at http://localhost:{PORT}")
        print(f"Car Parking Shades: http://localhost:{PORT}/car-parking-shades")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
