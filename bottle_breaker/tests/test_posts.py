# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
Tests for the posts module.
"""

import os

import pytest

from bottle_breaker._base_db import create_tables
from bottle_breaker.posts import Posts


@pytest.fixture
def posts_database():
    """Setup and teardown the database."""
    create_tables("testing_database.db")
    posts = Posts("testing_database.db")
    yield posts
    posts.close()
    os.remove("testing_database.db")


def test_create_tables(posts_database):
    """Test that we can create the tables."""
    assert os.path.exists("testing_database.db")


def test_create_two_posts(posts_database):
    """Test that creating a post works."""
    posts_database.make_post("user1", "content1")
    posts_database.make_post("user2", "content2")

    _posts = posts_database.get_posts()

    assert _posts[0]["by_user"] == "user1"
    assert _posts[0]["content"] == "content1"
    assert _posts[1]["by_user"] == "user2"
    assert _posts[1]["content"] == "content2"


def test_get_posts_for_a_user(posts_database):
    """Test that we can get posts for a specific user."""
    posts_database.make_post("user1", "content1")
    posts_database.make_post("user2", "content2")
    posts_database.make_post("user1", "content3")

    _posts = posts_database.get_posts_from_username("user1")

    assert len(_posts) == 2
    assert _posts[0]["by_user"] == "user1"
    assert _posts[0]["content"] == "content1"
    assert _posts[1]["by_user"] == "user1"
    assert _posts[1]["content"] == "content3"


def test_delete_a_post(posts_database):
    """Add a post, delete it, and assert the user has no posts."""
    posts_database.make_post("user1", "content1")
    posts_database.make_post("user2", "content2")
    posts_database.make_post("user1", "content3")

    _posts = posts_database.get_posts_from_username("user1")
    posts_database.delete_post(_posts[0]["id"])

    _posts = posts_database.get_posts_from_username("user1")
    assert len(_posts) == 1
    assert _posts[0]["by_user"] == "user1"
    assert _posts[0]["content"] == "content3"
