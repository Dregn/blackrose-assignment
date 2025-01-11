"""
Database repository for managing random numbers.
"""

import sqlite3

DB_FILE = "data.db"

def save_random_number(timestamp: str, value: int):
    """
    Saves a random number to the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO random_numbers (timestamp, value) VALUES (?, ?)", (timestamp, value))
    conn.commit()
    conn.close()
