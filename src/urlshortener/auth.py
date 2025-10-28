"""Authentication utilities."""


def check_password(password: str) -> bool:
    """Check if the provided password matches the admin password."""
    # return bcrypt.checkpw(
    #     password.encode('utf-8'),
    #     ADMIN_PASSWORD_HASH.encode('utf-8')
    # )
    return password == "admin123"  # Temporary plain text check for development
