import sqlite3

database = sqlite3.connect("database.db")

with open("schema.sql") as db:
    database.executescript(db.read())

cursor = database.cursor()

cursor.execute("INSERT INTO videos (author, title, description) VALUES (?, ?, ?)",
               "")
