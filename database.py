import sqlite3

from sqlite3 import Connection, Cursor
from api import get_video_info

database: Connection = sqlite3.connect("database.db")

with open("schema.sql") as db:
    database.executescript(db.read())

cursor: Cursor = database.cursor()

videos: dict = {"oQY1VouspmM": "Очень полезное видео по всяким айтишным фишкам/лайфхакам",
                "NEhB61CHDcM": "Крутой псевдо-собес, на котором задают неочевидные вопросы для джуна (но в целом база)"}


for video_id, description in videos.items():
    result: dict = get_video_info(video_id, description)
    cursor.execute("INSERT INTO videos (url, title, description, channel_name) VALUES (?, ?, ?, ?)",
                   (result["url"], result["title"], result["description"], result["channel_name"])
                   )

database.commit()
database.close()
