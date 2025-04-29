"""
Module to setup the database.
"""

import sqlite3 as sql


def setup_db():
    """Setup the database."""
    conn = sql.connect("db.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, password TEXT NOT NULL)"
    )

    conn.commit()
    conn.close()
