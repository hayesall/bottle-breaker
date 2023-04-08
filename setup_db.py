# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
First-time database setup for reproducibility.
"""

from time import sleep

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

db.posts.make_post("alice", "Hello, world!")
sleep(1)
db.posts.make_post("bob", "Hello, Alice!")
sleep(1)
db.posts.make_post(
    "eve",
    "<strong><em>Check this out</em></strong>: if you type your password in a post it will be invisible: <strong>********</strong> this is so cool!",
)
sleep(1)
db.posts.make_post("alice", "<strong>@bob</strong> hi bob!")
sleep(1)
db.posts.make_post("bob", "<strong>@alice</strong> lol hi alice")

db.posts.commit()

db.close()
