"""Database operations for URL shortener."""

import sqlite3
from typing import Optional
from urlshortener.config import DB_PATH


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_long_url(short_code: str) -> Optional[str]:
    """Get the long URL for a given short code."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()

    return row["long_url"] if row else None


def save_url(short_code: str, long_url: str) -> bool:
    """Save a new short code -> long URL mapping."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO urls (short_code, long_url) VALUES (?, ?)",
            (short_code, long_url)
        )

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def delete_url(short_code: str) -> bool:
    """Delete a URL mapping."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def get_all_urls() -> list[dict]:
    """Get all URL mappings."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT short_code, long_url, created_at FROM urls ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
