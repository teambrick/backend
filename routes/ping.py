from flask_restful import Resource

url = "/ping"

# class Ping(Resource):
def get(self):
    return "ping :)"
