from flask import Response

def not_found():
    return Response(status=404)

def error(status, message=None):
    response = {
        "success": False, 
        "code": status,
        "message": (message or HTTPStatus(status).phrase)
    }

    response = Response(json.dumps(response), status= (status if status else 400), mimetype="application/json", headers=headers)

    return response

def success(data=None, message=None):
    response = {
        "success": True, 
        "code": 200,
        "data": data,
        "message": (message or "Success")
    }

    if not data == None:
        response = Response(json.dumps(response), status=200, mimetype="application/json", headers=headers)
        return response
    else:
        return Response(status=204, mimetype="application/json", headers=headers)