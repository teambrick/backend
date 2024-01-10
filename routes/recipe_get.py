from flask.json import jsonify
from src.responses import not_found
from src import db
from flask import Response

url = "/recipe/<recipe_id>"


def get(recipe_id):
    cursor = db.getDb().cursor()
    cursor.execute(f"SELECT * FROM Recipes WHERE RecipeID={recipe_id}")
    res = cursor.fetchone()
    if res is None: return not_found()
    (_index, name, desc, method) = res
    return (jsonify(name=name, desc=desc, method=method), 200)
