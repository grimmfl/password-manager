"""Main"""
import os
from db_setup import setup_db
import passwords


if __name__ == "__main__":
    if "db.db" not in os.listdir():
        setup_db()

    id_ = passwords.create_password("Test", "Test", "Test", "Test1234")
    print(passwords.get_password(id_, "Test1234"))
