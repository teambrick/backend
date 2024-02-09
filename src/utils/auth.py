from flask import Flask
from flask import jsonify
from flask import request
import os
import db
import bcrypt
from utils.responses import error, success

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)



# Setup the Flask-JWT-Extended extension



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    cursor = db.connect().cursor()
    cursor.execute("SELECT * FROM Users WHERE UserName=%s", (username))
    res = cursor.fetchone()
    if res is None:
        # such GDPR
        return error(401, "User doesn't exist")
    (user_id, house_id, _username, pw_hash) = res
    if not bcrypt.checkpw(password, pw_hash):
        return error(401, "Incorrect username or password")


    access_token = create_access_token(identity=username)
    return success({"access_token":access_token})


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run()
