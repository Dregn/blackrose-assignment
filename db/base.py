"""
Database initialization logic for SQLite.
Creates tables if they do not exist.
"""

import sqlite3

DB_FILE = "data.db"

def init_db():
    """
    Initializes the SQLite database and creates tables if they don't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create table for random numbers
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS random_numbers (
            timestamp TEXT PRIMARY KEY,
            value INTEGER
        )
        """
    )
    conn.commit()
    conn.close()
