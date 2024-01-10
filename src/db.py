import sqlite3
from pathlib import Path
import os
from flask import g

if sqlite3.threadsafety == 0:
    raise Exception("sqlite3 is not being thread safe")

# handle creating the database if it doesn't exist

db_path = Path("./database.db")
if not db_path.is_file():
    if db_path.exists():
        raise Exception("./database.db exists but is not a regular file")
    cmd = os.system("touch ./database.db && cat src/sql/create.sql | sqlite3 database.db")
    if not cmd == 0:
        raise Exception("failed to create database or initialize it")

def getDb() -> sqlite3.Connection:
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(db_path)
    return db
