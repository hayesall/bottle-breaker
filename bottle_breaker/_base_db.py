# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
Base class for database tables.
"""

import sqlite3
from os import PathLike
from typing import Union


def create_tables(db_path: Union[str, PathLike] = "sample_database.db"):
    """First-time setup to create all tables in the database."""
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    with open("schema.sql", "r") as fh:
        curr.executescript(fh.read())
    conn.commit()


class BaseDB:
    """Base class to setup a database connection and cursor."""

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

    def repl(self):
        """Start a REPL for the database."""
        while True:
            command = input("sqlite3> ")
            if command == "exit":
                break
            self.curr.execute(command)
            print([(*row,) for row in self.curr.fetchall()])
            self.commit()
