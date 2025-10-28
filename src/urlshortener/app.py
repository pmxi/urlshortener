"""WSGI application for URL shortener."""

import os
from urllib.parse import parse_qs
from urlshortener import db, auth


def application(environ, start_response):
    """
    WSGI application entry point.

    This function is called by the WSGI server (gunicorn) for each request.

    Args:
        environ: Dictionary containing request information (headers, path, etc.)
        start_response: Callback to set response status and headers

    Returns:
        Iterable of bytes to send as response body
    """
    print("Received request:", environ.get('PATH_INFO', ''))

    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')

    # Route to appropriate handler
    if path == '/urlshorteneradmin':
        return handle_admin(environ, start_response)
    else:
        return handle_redirect(environ, start_response, path)


def handle_redirect(environ, start_response, path):
    """Handle short URL redirects."""
    # Remove leading slash
    short_code = path.lstrip('/')

    if not short_code:
        # Root path - return 404
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

    # Look up the URL
    long_url = db.get_long_url(short_code)

    if long_url:
        # Redirect to the long URL
        start_response('302 Found', [('Location', long_url)])
        return [b'']
    else:
        # Not found
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Short URL not found']


def handle_admin(environ, start_response):
    """Handle admin panel requests."""
    method = environ.get('REQUEST_METHOD', 'GET')

    if method == 'GET':
        # Show admin panel
        html = get_admin_html()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html)))
        ])
        return [html.encode('utf-8')]

    elif method == 'POST':
        # Handle form submission
        return handle_admin_post(environ, start_response)

    else:
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b'Method Not Allowed']


def handle_admin_post(environ, start_response):
    """Handle POST requests to admin panel."""
    try:
        # Read POST data
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        post_data = environ['wsgi.input'].read(content_length)
        params = parse_qs(post_data.decode('utf-8'))

        # Get form fields
        password = params.get('password', [''])[0]
        action = params.get('action', [''])[0]

        # Check password
        if not auth.check_password(password):
            start_response('401 Unauthorized', [('Content-Type', 'text/plain')])
            return [b'Invalid password']

        # Handle different actions
        if action == 'add':
            short_code = params.get('short_code', [''])[0]
            long_url = params.get('long_url', [''])[0]

            if short_code and long_url:
                db.save_url(short_code, long_url)

        elif action == 'delete':
            short_code = params.get('short_code', [''])[0]
            if short_code:
                db.delete_url(short_code)

        # Redirect back to admin panel
        start_response('303 See Other', [('Location', '/urlshorteneradmin')])
        return [b'']

    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f'Error: {str(e)}'.encode('utf-8')]


def get_admin_html() -> str:
    """Generate admin panel HTML."""
    urls = db.get_all_urls()

    # Read template file
    template_path = os.path.join(
        os.path.dirname(__file__),
        'templates',
        'admin.html'
    )

    try:
        with open(template_path, 'r') as f:
            template = f.read()

        # Generate URL list HTML
        url_rows = ''
        for url_data in urls:
            url_rows += f"""
            <tr>
                <td>{url_data['short_code']}</td>
                <td>{url_data['long_url']}</td>
                <td>{url_data['created_at']}</td>
                <td>
                    <form method="post" style="display:inline;">
                        <input type="hidden" name="password" id="delete-password-{url_data['short_code']}">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="short_code" value="{url_data['short_code']}">
                        <button type="submit" onclick="document.getElementById('delete-password-{url_data['short_code']}').value = document.getElementById('main-password').value;">Delete</button>
                    </form>
                </td>
            </tr>
            """

        return template.replace('{{url_rows}}', url_rows)

    except FileNotFoundError:
        # Fallback if template not found
        return "<h1>Admin Panel</h1><p>Template not found</p>"


# For gunicorn: this is what gets imported
# Run with: gunicorn urlshortener.app:application
