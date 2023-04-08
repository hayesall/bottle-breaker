# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

"""
Tests for the access control module, i.e.: test that we can setup users
and that those users can authenticate with a password.
"""

import os

import pytest

from bottle_breaker._base_db import create_tables
from bottle_breaker.access_control import Users


@pytest.fixture
def users_database():
    """Setup and teardown the database."""
    create_tables("testing_database.db")
    users = Users("testing_database.db")
    yield users
    users.close()
    os.remove("testing_database.db")


def test_create_tables(users_database):
    """Test that we can create the tables."""
    assert os.path.exists("testing_database.db")


def test_insert_a_user(users_database):
    """Test that we can insert a user into the database."""
    users_database.add_user("test_user", "test_password")
    assert users_database.get_usernames() == ["test_user"]


def test_insert_two_users(users_database):
    """Test that we can insert two users."""
    users_database.add_user("test_user_1", "tp1")
    users_database.add_user("test_user_2", "tp2")
    assert users_database.get_usernames() == ["test_user_1", "test_user_2"]


def test_verify_user_identity(users_database):
    """Test that we can verify a user by checking their password."""
    users_database.add_user("test_user_1", "tp1")
    assert users_database.verify_user("test_user_1", "tp1")


def test_verify_user_identity_bad_password(users_database):
    """Test that a bad password will fail."""
    users_database.add_user("test_user_1", "tp1")
    assert not users_database.verify_user("test_user_1", "tp2")
