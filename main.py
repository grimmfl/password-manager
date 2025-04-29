"""Main"""
import os
from db_setup import setup_db


if __name__ == "__main__":
    if "db.db" not in os.listdir():
        setup_db()
