from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from utils import db
from utils.responses import error, success

url = "/user/whoami"

@jwt_required()
def get():
    uid = get_jwt_identity()
    # (uid, hid, name, _)
    res = db.connect().cursor().execute("SELECT * FROM Users WHERE UserID = ?", (uid,)).fetchone()
    if res is None: return error(400)
    (uid, hid, name, _) = res
    return success({"user_id":uid, "house_id":hid, "username":name})
