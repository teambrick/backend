url = "/ingredient/<id>"

from utils import db
from utils.responses import success

def get(idx):
    [name, unit, data] = db.connect().cursor().execute(f"SELECT IngredientName, ReadableUnit, Data FROM Ingredients WHERE IngredientID={idx}").fetchone()

    return success({"name":name, "unit":unit, "data":data})
