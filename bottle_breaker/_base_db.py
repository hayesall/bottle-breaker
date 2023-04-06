# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
Base class for database tables.
"""

import sqlite3
from os import PathLike
from typing import Union


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
