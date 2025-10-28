# URL Shortener

A simple WSGI-based URL shortening service for parasmittal.com.

## Quick Start

### Prerequisites

- Python 3.13+ installed
- `uv` package manager installed (https://github.com/astral-sh/uv)

### Running Locally

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/urlshortener
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   This will create a `.venv` virtual environment and install all dependencies (gunicorn, bcrypt).

3. **Run the development server:**
   ```bash
   uv run gunicorn urlshortener.app:application --bind 127.0.0.1:8000 --reload
   ```

   You should see output like:
   ```
   [INFO] Starting gunicorn 23.0.0
   [INFO] Listening at: http://127.0.0.1:8000
   ```

4. **Test the application:**

   Open your browser and go to:
   - **Admin Panel:** http://localhost:8000/urlshorteneradmin
   - **Default password:** `admin` (**CHANGE THIS IN PRODUCTION!**)

5. **Create your first short URL:**
   - Enter the admin password: `admin`
   - Fill in "Short Code" (e.g., `gh`)
   - Fill in "Long URL" (e.g., `https://github.com/parasmittal`)
   - Click "Add/Update URL"

6. **Test the redirect:**
   - Visit: http://localhost:8000/gh
   - You should be redirected to the long URL

### Stopping the Server

Press `Ctrl+C` in the terminal where gunicorn is running.

## Project Structure

```
urlshortener/
├── src/
│   └── urlshortener/
│       ├── __init__.py          # Package initialization
│       ├── app.py               # WSGI application (main entry point)
│       ├── db.py                # SQLite database operations
│       ├── auth.py              # Password authentication
│       ├── config.py            # Configuration settings
│       └── templates/
│           └── admin.html       # Admin panel HTML template
├── .venv/                       # Virtual environment (created by uv)
├── pyproject.toml               # Project dependencies (managed by uv)
├── .python-version              # Python version (3.13)
├── urls.db                      # SQLite database (created at runtime)
└── README.md                    # This file
```

## Configuration

### Change the Admin Password

**Method 1: Generate a new password hash**

```bash
uv run python -c "from urlshortener.auth import hash_password; print(hash_password('your_new_password'))"
```

This will output something like:
```
$2b$12$abcd1234...xyz
```

**Method 2: Set via environment variable**

```bash
export ADMIN_PASSWORD_HASH='$2b$12$abcd1234...xyz'
uv run gunicorn urlshortener.app:application --bind 127.0.0.1:8000
```

### Change Database Location

By default, the database is stored at `urls.db` in the project root. To change it:

```bash
export DB_PATH=/path/to/your/database.db
uv run gunicorn urlshortener.app:application --bind 127.0.0.1:8000
```

## Production Deployment

### Running with Gunicorn (Production)

```bash
gunicorn urlshortener.app:application \
  --workers 4 \
  --bind 127.0.0.1:8000 \
  --access-logfile - \
  --error-logfile - \
  --daemon
```

**Important:**
- Set `ADMIN_PASSWORD_HASH` environment variable with your own password
- Use a process manager like `systemd` to keep it running
- Run behind Nginx as a reverse proxy (see below)

### Nginx Configuration

Add this to your Nginx config to integrate with your existing parasmittal.com site:

```nginx
server {
    listen 80;
    server_name parasmittal.com;

    root /path/to/parasonepage;

    # Try static files first
    location / {
        try_files $uri $uri/ @urlshortener;
    }

    # Admin panel
    location /urlshorteneradmin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Fallback to URL shortener for non-existent files
    location @urlshortener {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This configuration:
1. Serves static files from your existing site first
2. If a file doesn't exist, passes the request to the URL shortener
3. Admin panel is always handled by the URL shortener app

### Systemd Service (Linux)

Create `/etc/systemd/system/urlshortener.service`:

```ini
[Unit]
Description=URL Shortener WSGI Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/urlshortener
Environment="PATH=/path/to/urlshortener/.venv/bin"
Environment="ADMIN_PASSWORD_HASH=your_hash_here"
Environment="DB_PATH=/var/lib/urlshortener/urls.db"
ExecStart=/path/to/urlshortener/.venv/bin/gunicorn urlshortener.app:application --workers 4 --bind 127.0.0.1:8000
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable urlshortener
sudo systemctl start urlshortener
sudo systemctl status urlshortener
```

## How Python Imports Work

With the src layout, Python imports use the full package path:

```python
# In any file within src/urlshortener/
from urlshortener.db import get_url        # Absolute import
from urlshortener.auth import check_password

# OR using relative imports (when inside the package)
from .db import get_url                    # Relative import
from .auth import check_password
```

The `src/` directory is automatically added to Python's path by uv when you run `uv run`.

## Development

### Running Tests (TODO)

```bash
uv run pytest
```

### Code Style (TODO)

```bash
uv run ruff check .
uv run ruff format .
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'urlshortener'`:
- Make sure you're using `uv run` to run commands
- OR activate the virtual environment: `source .venv/bin/activate`

### Database Errors

If the database gets corrupted, simply delete `urls.db` and restart the server. A new database will be created automatically.

### Permission Errors

Make sure the application has write permissions to create `urls.db` in the project directory (or wherever `DB_PATH` points).
