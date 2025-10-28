"""Configuration settings for the URL shortener."""

import os

# Database configuration
DB_PATH = os.environ.get("DB_PATH", "urls.db")
