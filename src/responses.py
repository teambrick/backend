from flask.json import jsonify

def not_found():
    return (jsonify({"status":404}), 404)
