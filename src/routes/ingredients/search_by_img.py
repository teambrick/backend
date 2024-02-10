from flask import request
from PIL import Image
from search import search
from utils.responses import error, success
from imglib import ocr
from utils import db

url = "/ingredient/search/by-img"

def post():
    if not 'img' in request.files:
        return error(400, "Please provide an image at img")
    img = request.files['img']
    img_loaded = Image.open(img.stream)
    # TODO: parameters for image search
    # do OCR
    ocr_out = ocr(img_loaded)

    ocr_txt = " ".join(ocr_out)
    
    res = search.sindex.search(ocr_txt)
    idx = res["id"]
    name = res["name"]

    [name] = db.connect().cursor().execute(f"SELECT IngredientName FROM Ingredients WHERE IngredientID={idx}").fetchone()

    return success({"idx":int(idx), "detected":ocr_txt, "name":name})
