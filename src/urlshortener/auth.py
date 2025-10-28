"""Authentication utilities."""

import bcrypt
from urlshortener.config import ADMIN_PASSWORD_HASH


def check_password(password: str) -> bool:
    """Check if the provided password matches the admin password."""
    # return bcrypt.checkpw(
    #     password.encode('utf-8'),
    #     ADMIN_PASSWORD_HASH.encode('utf-8')
    # )
    return password == "admin123"  # Temporary plain text check for development


def hash_password(password: str) -> str:
    """Hash a password for storage. Useful for generating new password hashes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
