#!/usr/bin/env python
"""Management script for URL shortener database operations."""

import sys
from urlshortener.db import init_db, get_all_urls
from urlshortener.config import DB_PATH


def cmd_init():
    """Initialize the database."""
    print(f"Initializing database at: {DB_PATH}")
    init_db()
    print("✓ Database initialized successfully")


def cmd_status():
    """Show database status."""
    try:
        urls = get_all_urls()
        print(f"Database: {DB_PATH}")
        print(f"Total URLs: {len(urls)}")
        print("\nExisting URLs:")
        if urls:
            for url in urls:
                print(f"  /{url['short_code']} → {url['long_url']}")
        else:
            print("  (no URLs yet)")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Database may not be initialized. Run: uv run python manage.py init")


def cmd_help():
    """Show help message."""
    print("""
URL Shortener Management Tool

Usage:
    uv run python manage.py <command>

Commands:
    init        Initialize the database (creates tables)
    status      Show database status and list all URLs
    help        Show this help message

Examples:
    uv run python manage.py init      # Create database
    uv run python manage.py status    # Check database
    """)


if __name__ == "__main__":
    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "help": cmd_help,
    }

    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(1)

    command = sys.argv[1]

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        cmd_help()
        sys.exit(1)
