import sqlite3

from api import get_video_info
from config import SECRET_KEY
from sqlite3 import Connection

from flask import Flask, render_template, request, url_for, flash, redirect, Response
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


def get_db_connection() -> Connection:
    connection: Connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def get_video(video_id: int) -> dict:
    connection: Connection = get_db_connection()
    video = connection.execute("SELECT * FROM videos WHERE id = ?",
                               (video_id,)).fetchone()
    connection.close()
    if video is None:
        abort(404)
    return video


@app.route("/home")
def home() -> str:
    connection = get_db_connection()
    videos = connection.execute("SELECT * FROM videos").fetchall()
    connection.close()
    return render_template("index.html", videos=videos)


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/<int:video_id>")
def video(video_id: int) -> str:
    video: dict = get_video(video_id)
    return render_template("video.html", video=video)


@app.route("/add_video", methods=("GET", "POST"))
def add_video() -> Response | str:
    if request.method == "POST":
        video_id: str = request.form["video_id"]
        description: str = request.form["description"]

        if not video_id:
            flash("ID видео не заполнено")
        elif not description:
            flash("Описание видео не заполнено")
        else:
            video: dict = get_video_info(video_id, description)

            connection: Connection = get_db_connection()
            connection.execute("INSERT INTO videos (url, title, description, channel_name) VALUES (?, ?, ?, ?)",
                               (video["url"], video["title"], video["description"], video["channel_name"]))
            connection.commit()
            connection.close()
            return redirect(url_for("home"))

    return render_template("add_video.html")


@app.route("/<int:video_id>/edit_video", methods=("GET", "POST"))
def edit_video(video_id) -> Response | str:
    video: dict = get_video(video_id)

    if request.method == "POST":
        description: str = request.form["description"]

        if not description:
            flash("Описание не было заполнено.")
        else:
            conn: Connection = get_db_connection()
            conn.execute("UPDATE videos SET description = ? WHERE id = ?",
                         (description, video_id))
            conn.commit()
            conn.close()
            return redirect(url_for("home"))

    return render_template("edit_video.html", video=video)


@app.route("/<int:video_id>/delete_video", methods=("POST",))
def delete_video(video_id: int) -> Response:
    video: dict = get_video(video_id)
    conn: Connection = get_db_connection()
    conn.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
    flash(f'Видео {video["title"]} было успешно удалено')
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
