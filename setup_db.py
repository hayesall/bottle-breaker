# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
First-time database setup for reproducibility.
"""

from bottle_breaker.access_control import create_tables
from bottle_breaker.app import Database

# Default location when 'app.root_path' runs
DB_PATH = "bottle_breaker/sample_database.db"

create_tables(DB_PATH)

db = Database(DB_PATH)
db.users.add_user("alice", "alice_password")
db.users.add_user("bob", "bob_password")
db.users.add_user("eve", "eve_password")

db.users.commit()
db.close()
