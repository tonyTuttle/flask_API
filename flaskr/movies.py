"""https://flask.palletsprojects.com/en/2.3.x/tutorial/blog/"""

import json
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("movies", __name__)


@bp.route("/items", methods=("POST",))
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            return jsonify({"error": error})
        else:
            db = get_db()
            db.execute(
                "INSERT INTO movie (title, year)" " VALUES (?, ?)",
                (title, year),
            )
            db.commit()
            return jsonify({"message": "Item created"})

    return jsonify({"message: Expected a POST"})


@bp.route("/items", methods=("GET",))
def get(id=None):
    if request.method == "GET":
        db = get_db()
        cursor = db.cursor()
        if id:
            cursor.execute("SELECT * FROM movie WHERE id = ?", (id,))
        else:
            cursor.execute("SELECT * FROM movie")
        movies = cursor.fetchall()
        columns = [c[0] for c in cursor.description]
        movie_list = [dict(zip(columns, movie)) for movie in movies]
        return jsonify(movie_list)

    return jsonify({"message": "Expected a POST"})


# @bp.route("/items", methods=("GET",))
# def get_by_id(id: int):
#     if request.method == "GET":
#         db = get_db()
#         cursor = db.cursor()

#         movie = cursor.fetchone()
#         columns = [c[0] for c in cursor.description]
#         movie_list = [dict(zip(columns, m)) for m in movie]
#         return jsonify(movie_list)

#     return jsonify({"message": "Expected a GET"})
