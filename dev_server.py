"""Development server with debugger support.

This simple WSGI server is easier to debug than gunicorn because it runs
in a single process without worker spawning.

Usage:
    python dev_server.py
    OR
    uv run python dev_server.py
    OR
    Press F5 in VS Code to start debugging
"""

from wsgiref.simple_server import make_server
from urlshortener.app import application

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8000

    print(f"Starting development server on http://{HOST}:{PORT}")
    print(f"Admin panel: http://{HOST}:{PORT}/urlshorteneradmin")
    print("Press Ctrl+C to stop")
    print()
    print("This server supports VS Code debugging - set breakpoints and press F5!")

    with make_server(HOST, PORT, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
