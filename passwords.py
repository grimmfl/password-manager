"""Module to handle passwords."""
import base64
import hashlib
import sqlite3 as sql

from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(password: str, primary_password: str):
    """
    Encrypt a password
    :param password: The password to encrypt
    :param primary_password: The primary password to use for encryption
    :return: The base4 encoded encrypted password
    """
    key = hashlib.sha256(primary_password.encode()).digest()

    raw = str.encode(pad(password))  # convert str to byte
    init_vector = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    return base64.b64encode(init_vector + cipher.encrypt(raw))


def decrypt(encrypted: str, primary_password: str) -> str:
    """
    Decrypt a password
    :param encrypted: The encrypted password
    :param primary_password: The primary password to use for decryption
    :return: The decrypted password
    """
    key = hashlib.sha256(primary_password.encode()).digest()

    enc = base64.b64decode(encrypted)
    init_vector = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    return unpad(cipher.decrypt(enc[16:])).decode()


def get_password(password_id: int, primary_password: str) -> str:
    """
    Get a password by id and the primary password
    :param password_id: The password id
    :param primary_password: The primary password
    :return: The password
    """
    conn = sql.connect("db.db")
    cursor = conn.cursor()

    password = cursor.execute(
        "SELECT password FROM passwords WHERE id = ?",
        (password_id,)
    ).fetchone()[0]

    conn.close()

    return decrypt(password, primary_password)


def create_password(
        website: str,
        user: str,
        password: str,
        primary_password: str
) -> int:
    """
    Create a new password
    :param website: The website
    :param user: The username / email
    :param password: The password
    :param primary_password: The primary password to use for encryption
    :return: The password id
    """
    encrypted = encrypt(password, primary_password)

    conn = sql.connect("db.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO passwords (website, user, password) VALUES (?, ?, ?)",
        (website, user, encrypted)
    )
    id_ = cursor.lastrowid

    conn.commit()

    conn.close()

    return id_
