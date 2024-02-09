url = "/user"

from flask import request
from cerberus import Validator
from utils import db

from utils.responses import error, success

import bcrypt

from base64 import b64encode

schema = {"username":{"type":"string"}, "password":{"type":"string"}, "house_id":{"type":"integer"}}
v = Validator()


def post():
    if not v(request.json, schema=schema):
        return error(422, v.errors)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    house_id = request.json.get("house_id", None)
    
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Households WHERE HouseholdID={house_id}")
    if cursor.fetchone() is None:
        return error(400, "Household doesn't exist")

    password_hash = str(bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt()), "utf-8")
    
    cursor.execute(f"INSERT INTO Users (HouseholdID, UserName, Password) VALUES (?, ?, ?)", (house_id, username, password_hash))
    conn.commit()


    return success()
