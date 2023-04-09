# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
Handle making and getting posts.
"""

from sqlite3 import OperationalError
from bottle_breaker._base_db import BaseDB


class Posts(BaseDB):
    def get_posts(self):
        """Get all posts."""

        try:
            self.curr.execute("SELECT * FROM posts ORDER BY posts.post_time DESC")
            return self.curr.fetchall()
        except OperationalError:
            return []

    def get_posts_from_username(self, username: str):
        """Get the posts made by a specific user."""

        try:
            self.curr.execute(
                "SELECT * FROM posts WHERE by_user = ? ORDER BY post_time DESC",
                (username,),
            )
            return self.curr.fetchall()
        except OperationalError:
            return []

    def make_post(self, author, content):
        self.curr.execute(
            "INSERT INTO posts (by_user, content) VALUES (?, ?)",
            (author, content),
        )
        self.commit()

    def delete_post(self, post_id: int):
        self.curr.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.commit()
