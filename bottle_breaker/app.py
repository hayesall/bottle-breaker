# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

from os import PathLike, path
from typing import Union

from flask import Flask, g, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from bottle_breaker.access_control import (
    AnonymousUser,
    ChangeUsernameForm,
    LoginForm,
    RegisterForm,
    User,
    Users,
)
from bottle_breaker.posts import Posts


def load_secret_key() -> str:
    """In a real application, this should be stored more securely, such as in
    an environment variable."""
    return "818d8dccdac011b38d88397c44868960f2583e44b5d46e30e406c4b3543daf83"


app = Flask(__name__)
app.secret_key = load_secret_key()

login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser
login_manager.init_app(app)

DB_PATH = path.join(app.root_path, "sample_database.db")


class Database:
    """Database object, implementing something like the MVC pattern."""

    def __init__(self, db_path: Union[str, PathLike] = "sample_database.db"):
        self._db_path = db_path

    @property
    def users(self):
        return Users(self._db_path)

    @property
    def posts(self):
        return Posts(self._db_path)

    def close(self):
        self.users.close()
        self.posts.close()

    def __del__(self):
        self.close()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database(DB_PATH)
    return db


@login_manager.user_loader
def load_user(username):
    with app.app_context():
        db = get_db()
        if username not in db.users.get_usernames():
            return
    user = User()
    user.DB_PATH = DB_PATH
    user.id = username
    return user


@app.route("/")
def index():
    """Home page, showing all posts when the user is logged in or a
    registration form otherwise"""
    with app.app_context():
        db = get_db()
        posts = db.posts.get_posts()
    return render_template("index.html", posts=posts, form=RegisterForm())


@app.route("/make-post", methods=["POST"])
@login_required
def make_post():
    """Page for posting a new message."""
    with app.app_context():
        db = get_db()
        db.posts.make_post(request.args["author"], request.form["makeNewPost"])
    return redirect(url_for("index"))


@app.route("/delete-post/<username>/<int:post_id>", methods=["POST"])
@login_required
def delete_post(username: str = None, post_id: int = None):
    """Delete a post."""
    with app.app_context():
        db = get_db()
        db.posts.delete_post(post_id)
    return redirect(url_for("user_profile", username=username))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def user_settings():
    """User settings page."""

    form = ChangeUsernameForm(request.form)

    with app.app_context():
        db = get_db()

        if form.validate_on_submit():
            if (
                db.users.change_username(
                    current_user.id, form.new_username.data
                )
                == "Success"
            ):
                return redirect(
                    url_for("login", username=form.new_username.data)
                )
            # User already exists. Notify the user.
            return render_template(
                "settings.html",
                form=form,
                username_error="User already exists, please choose something else.",
            )
        return render_template("settings.html", form=form)


@app.route("/profile/<username>")
@login_required
def user_profile(username=None):
    """User profile page, showing all of their posts."""
    with app.app_context():
        db = get_db()
        posts = db.posts.get_posts_from_username(username)
    return render_template("user_profile.html", username=username, posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register that the user createa a new account."""
    form = RegisterForm(request.form)
    with app.app_context():
        db = get_db()
        if form.validate_on_submit():
            if (
                db.users.add_user(form.username.data, form.password.data)
                == "Success"
            ):
                return redirect(url_for("login", username=form.username.data))
            # User already exists. Notify the user.
            return render_template(
                "index.html",
                form=form,
                username_error="User already exists.",
            )
        return render_template("index.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page using the LoginForm."""

    form = LoginForm(request.form)

    with app.app_context():
        db = get_db()

        if form.validate_on_submit():
            if db.users.verify_user(form.username.data, form.password.data):
                user = User()
                user.id = form.username.data
                login_user(user)

                return redirect(url_for("index"))
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(401)
def user_unauthorized(err):
    return render_template("401.html"), 401


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404
