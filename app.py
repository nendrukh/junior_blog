import sqlite3

from api import get_video_info
from config import SECRET_KEY

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def get_video(video_id):
    connection = get_db_connection()
    video = connection.execute("SELECT * FROM videos WHERE id = ?",
                               (video_id,)).fetchone()
    connection.close()
    if video is None:
        abort(404)
    return video


@app.route("/home")
def home():
    connection = get_db_connection()
    videos = connection.execute("SELECT * FROM videos").fetchall()
    connection.close()
    return render_template("index.html", videos=videos)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/<int:video_id>")
def video(video_id):
    video = get_video(video_id)
    return render_template("video.html", video=video)


@app.route("/add_video", methods=("GET", "POST"))
def add_video():
    if request.method == "POST":
        video_id = request.form["video_id"]
        description = request.form["description"]

        if not video_id:
            flash("ID видео не заполнено")
        elif not description:
            flash("Описание видео не заполнено")
        else:
            video = get_video_info(video_id, description)

            connection = get_db_connection()
            connection.execute("INSERT INTO videos (url, title, description, channel_name) VALUES (?, ?, ?, ?)",
                               (video["url"], video["title"], video["description"], video["channel_name"]))
            connection.commit()
            connection.close()
            return redirect(url_for("home"))

    return render_template("add_video.html")


if __name__ == "__main__":
    app.run(debug=True)
