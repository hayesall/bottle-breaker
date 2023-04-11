# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

import secrets
from datetime import datetime
from hashlib import pbkdf2_hmac
from sqlite3 import IntegrityError

from flask_login import AnonymousUserMixin, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

from bottle_breaker._base_db import BaseDB


class Users(BaseDB):
    """User management and access control."""

    HASHING_ITERATIONS = 500_000

    def get_usernames(self):
        self.curr.execute("SELECT username FROM users")
        return [user["username"] for user in self.curr.fetchall()]

    def delete_user(self, username: str):
        self.curr.execute("PRAGMA foreign_keys = ON;")
        self.curr.execute("DELETE FROM users WHERE username = ?;", (username,))
        self.commit()

    def change_username(self, old_username: str, new_username: str):
        """Change a user's username, returning an error if the username
        is already taken.

        This also needs to update the `posts` table to reflect the
        changed username, which should be handled by the database
        foreign keys + cascading update.
        """

        try:
            script = f"PRAGMA foreign_keys = ON; UPDATE users SET username = '{new_username}' WHERE username = '{old_username}';"
            self.curr.executescript(script)
            self.commit()

            return "Success"

        except IntegrityError:
            return "Username already exists"

    def add_user(
        self,
        username: str,
        password: str,
    ) -> str:
        """Add a new user, returning a temporary password or a chosen password."""

        salt = secrets.token_hex(32)

        hashed_password = pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), self.HASHING_ITERATIONS
        )

        try:
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
            return "Success"

        except IntegrityError:
            return "Username already exists"

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

        return secrets.compare_digest(hashed_password, user_hash)


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        [
            validators.DataRequired(),
            validators.EqualTo("password", message="Passwords must match"),
        ],
    )


class ChangeUsernameForm(FlaskForm):
    new_username = StringField("New Username", [validators.DataRequired()])


class User(UserMixin):
    DB_PATH = "sample_database.db"


class AnonymousUser(AnonymousUserMixin):
    pass
