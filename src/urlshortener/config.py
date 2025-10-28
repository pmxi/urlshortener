"""Configuration settings for the URL shortener."""

import os

# Database configuration
DB_PATH = os.environ.get("DB_PATH", "urls.db")

# Admin authentication
# This should be set via environment variable in production
# Generate hash with: python -c "import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())"
ADMIN_PASSWORD_HASH = os.environ.get(
    "ADMIN_PASSWORD_HASH",
    # Default: "admin" - CHANGE THIS IN PRODUCTION
    "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzXqQx3rGu"
)
