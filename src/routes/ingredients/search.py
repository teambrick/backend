from flask import request
from search import search
from utils.responses import error, success
from utils import db


url = "/ingredient/search"

def get():
    query = request.args.get("q", default="")
    if query == "":
        return error(400, "No search string provided")
    print("Searching for", query)
    (idx, inv_conf) = list(search.sindex.search(query))[0]
    # res = search.sindex.search(query)
    if "full" in request.args.keys():
        [name, unit, data] = db.connect().cursor().execute(f"SELECT IngredientName, ReadableUnit, Data FROM Ingredients WHERE IngredientID={idx}").fetchone()
        return success({"id":int(idx), "name":name, "unit":unit, "data":data, "inv_conf":float(inv_conf)})
    return success({"id":int(idx), "inv_conf":float(inv_conf)})
    
