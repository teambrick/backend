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
    dbCreation = sqlite3.connect(db_path) # make the database
    with open("./src/utils/sql/create.sql", "r") as sqlFile:
        sql = sqlFile.read()
        cursor = dbCreation.cursor()
        cursor.executescript(sql)
        dbCreation.commit()
        dbCreation.close()
        
    #cmd = os.system("touch ./database.db && cat src/sql/create.sql | sqlite3 database.db")
    #if not cmd == 0:
    #    raise Exception("failed to create database or initialize it")
    # ^ THIS IS NOT NEEDED, SQLITE 3 AUTOMATICALLY CREATES A DATABASE IF ONE DOESN'T EXIST also it doesn't work on windows :) - that is a skill issue <3

def connect() -> sqlite3.Connection:
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(db_path, check_same_thread=False)
    return db
