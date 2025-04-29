"""
Module handling primary user authentication.
"""

import sqlite3 as sql

from argon2 import PasswordHasher


def create_user(password: str):
    """
    Create a new primary user.
    :param password: The password to hash and store.
    """
    password_hasher = PasswordHasher()
    hashed = password_hasher.hash(password)

    conn = sql.connect("db.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (password) VALUES (?)", (hashed,))

    conn.commit()

    conn.close()


def authenticate(password: str) -> int:
    """
    Authenticate a primary user.
    :param password: The password to authenticate.
    :return: The user ID if successful, -1 otherwise.
    """
    conn = sql.connect("db.db")
    cursor = conn.cursor()

    users = cursor.execute("SELECT * FROM users").fetchall()

    conn.close()

    password_hasher = PasswordHasher()

    for user in users:
        if password_hasher.verify(user[1], password):
            return user[0]

    return -1
