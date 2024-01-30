from flask import request
from search import search
from utils.responses import error, success



url = "/ingredient/search"

def get():
    query = request.args.get("q", default="")
    if query == "":
        return error(400, "No search string provided")
    print("Searching for", query)
    (idx, inv_conf) = list(search.sindex.search(query))[0]
    return success({"id":int(idx), "inv_conf":float(inv_conf)})
    
