# from src import db
from flask import request
from src import db
import bcrypt
from uuid import uuid5

authed_users = {}

def user_auth():
    global authed_users
    if request.authorization is None:
        return 401
    auth = request.authorization
    if not auth.haskey("Bearer"):
        return 401
    if auth["Bearer"] in authed_users:
        return authed_users[auth["Bearer"]]
    else:
        return 498

def invalidate_token(token):
    global authed_users
    if token in authed_users: del authed_users[token]
def invalidate_all():
    global authed_users
    authed_users = {}

def login(user, passw):
    global authed_users
    crs = db.getDb().cursor()
    cursor.execute(f"SELECT * FROM Users WHERE Username={user}")
    res = cursor.fetchone()
    if res is None: return False
    [id, household_id, username, passwd_src] = res
    if bcrypt.checkpw(passw, passwd_src):
        token = uuid5()
        authed_users[token] = user
        return token
    else: return False
