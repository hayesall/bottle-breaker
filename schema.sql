-- Copyright © 2023 Alexander L. Hayes
-- MIT License or Apache 2.0 License, at your choosing

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

-- A user has a unique id, a username, a hashed password, a salt value, and a time stamp for the last password reset
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(15),
    password_hash VARCHAR(100),
    salt VARCHAR(100),
    last_reset TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Posts are global, associated with a user, and posts are deleted if a user is deleted
CREATE TABLE posts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    by_user INTEGER NOT NULL,
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    FOREIGN KEY(by_user) REFERENCES users(id) ON UPDATE CASCADE
);
