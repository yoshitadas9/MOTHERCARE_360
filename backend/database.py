import sqlite3

DATABASE = "mothercare.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    return db
    