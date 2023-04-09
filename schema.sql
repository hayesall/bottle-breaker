-- Copyright © 2023 Alexander L. Hayes
-- MIT License or Apache 2.0 License, at your choosing


DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

-- A user has a unique username, a hashed password, a salt value, and a time stamp for the last password reset
CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY,
    password_hash TEXT,
    salt TEXT,
    last_reset TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Posts are global, associated with a user, and posts are deleted if a user is deleted
CREATE TABLE posts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    by_user TEXT NOT NULL,
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    CONSTRAINT user_foreign_key
        FOREIGN KEY (by_user)
        REFERENCES users (username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
