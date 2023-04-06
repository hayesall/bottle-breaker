# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

import secrets
import sqlite3
from datetime import datetime
from hashlib import pbkdf2_hmac
from os import PathLike
from typing import Optional, Union

from flask_login import AnonymousUserMixin, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


def create_tables(db_path: Union[str, PathLike] = "sample_database.db"):
    """First-time setup to create all tables in the database."""
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    with open("schema.sql", "r") as fh:
        curr.executescript(fh.read())
    conn.commit()


class Users:
    """User management and access control."""

    HASHING_ITERATIONS = 500_000

    def __init__(self, db_path: Union[str, PathLike] = "sample_database.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.curr = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def get_users(self):
        self.curr.execute("SELECT display_name, username, email FROM users")
        return self.curr.fetchall()

    def get_usernames(self):
        self.curr.execute("SELECT username FROM users")
        return [user["username"] for user in self.curr.fetchall()]

    def set_display_name(self, username: str, display_name: str):
        self.curr.execute(
            "UPDATE users SET display_name = ? WHERE username = ?",
            (display_name, username),
        )
        self.commit()

    def add_user(
        self,
        username: str,
        password: Optional[str] = None,
    ) -> str:
        """Add a new user, returning a temporary password or a chosen password."""

        salt = secrets.token_hex(32)

        if password is None:
            password = secrets.token_hex(4)

        hashed_password = pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), self.HASHING_ITERATIONS
        )

        self.curr.execute(
            "INSERT INTO users (username, password_hash, salt, last_reset) VALUES (?, ?, ?, ?)",
            (
                username,
                hashed_password,
                salt,
                datetime.now(),
            ),
        )
        self.commit()

        return password

    def verify_user(self, username: str, password: str):
        """Returns True if the user exists and their password is correct."""

        if not self.curr.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone():
            return False

        user_hash, salt = self.curr.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        hashed_password = pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            self.HASHING_ITERATIONS,
        )

        return hashed_password == user_hash


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


class User(UserMixin):
    DB_PATH = "sample_database.db"


class AnonymousUser(AnonymousUserMixin):
    pass