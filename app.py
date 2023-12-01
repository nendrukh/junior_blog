import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/home")
def home():
    connection = get_db_connection()
    videos = connection.execute("SELECT * FROM videos").fetchall()
    connection.close()
    return render_template("index.html", videos=videos)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
