import sqlite3
from api import result

database = sqlite3.connect("database.db")

with open("schema.sql") as db:
    database.executescript(db.read())

cursor = database.cursor()

for url, value in result.items():
    cursor.execute("INSERT INTO videos (url, title, description, channel_name) VALUES (?, ?, ?, ?)",
                   (url, value["title"], value["description"], value["channel_name"])
                   )

database.commit()
database.close()
