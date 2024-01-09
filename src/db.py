import sqlite3

if sqlite3.threadsafety == 0:
    raise Exception("sqlite3 is not being thread safe")

