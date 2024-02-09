# TODO: urlparams and more

from flask import request
from utils import db
import bcrypt

from flask_jwt_extended import create_access_token

from utils.responses import error, success
from cerberus import Validator

url = "/auth/login"

schema = {"username":{"type":"string"}, "password":{"type":"string"}, "house_id":{"type":"integer"}}
v = Validator(schema)

def post():
    if not v.validate(request.json):
        return error(422, v.errors)
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    cursor = db.connect().cursor()
    cursor.execute("SELECT * FROM Users WHERE UserName = ?", (username,))
    res = cursor.fetchone()
    if res is None:
        # such GDPR
        return error(401, "User doesn't exist")
    (user_id, house_id, _username, pw_hash) = res
    if not bcrypt.checkpw(bytes(password, "utf-8"), bytes(pw_hash, "utf-8")):
        return error(401, "Incorrect username or password")


    access_token = create_access_token(identity=user_id)
    return success({"access_token":access_token})
