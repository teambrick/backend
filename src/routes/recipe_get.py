from utils.responses import error, success
from utils import db

url = "/recipe/<recipe_id>"


def get(recipe_id):
    cursor = db.connect().cursor()
    cursor.execute(f"SELECT * FROM Recipes WHERE RecipeID={recipe_id}")
    res = cursor.fetchone()
    if res is None: return error(404)
    (_index, name, desc, method) = res
    return success({
        "name": name,
        "description": desc,
        "method": method
    })
