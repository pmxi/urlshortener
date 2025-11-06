"""Database operations for URL shortener."""

import sqlite3
from contextlib import contextmanager
from typing import Optional
from urlshortener.config import DB_PATH


@contextmanager
def get_connection():
    """Get a database connection as a context manager."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Initialize the database schema."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                short_code TEXT PRIMARY KEY,
                long_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_long_url(short_code: str) -> Optional[str]:
    """Get the long URL for a given short code."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
        row = cursor.fetchone()
        return row["long_url"] if row else None


def save_url(short_code: str, long_url: str) -> bool:
    """Save a new short code -> long URL mapping."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO urls (short_code, long_url) VALUES (?, ?)",
                (short_code, long_url)
            )
        return True
    except sqlite3.Error:
        return False


def delete_url(short_code: str) -> bool:
    """Delete a URL mapping."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
        return True
    except sqlite3.Error:
        return False


def get_all_urls() -> list[dict]:
    """Get all URL mappings."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT short_code, long_url, created_at FROM urls ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
