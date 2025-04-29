"""
Module to set up the database.
"""

import sqlite3 as sql


def setup_db():
    """Set up the database."""
    conn = sql.connect("db.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE passwords ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
            "website TEXT NOT NULL,"
            "user TEXT NOT NULL,"
            "password TEXT NOT NULL"
        ")"
    )

    conn.commit()
    conn.close()
