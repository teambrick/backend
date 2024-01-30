from pathlib import Path
import importlib.util
import flask

app = flask.Flask(__name__)

setattr(__builtins__, "app", app)

from flask import g


valid_tokens = {}

# do not ask, i will not be able to answer
# this is my beautiful child and i love it
def import_path(path: Path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    if spec is None:
        raise Exception("file not found: " + str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

methods = ["get", "post", "put"]

# this is the beautiful twin
def cursed_importing():
    result = list(Path("src/routes/").rglob("*.py"))
    for k in result:
        mod = import_path(k)
        if "url" not in mod.__dict__.keys(): continue
        mnice = {k:v for k, v in mod.__dict__.items() if k in methods}
        print(mnice)
        for k,v in mnice.items():
          print(f"{k.upper()} {mod.url}")
          app.add_url_rule(mod.url, endpoint=mod.url, methods=[k.upper()], view_func=v)
  
def main():
  cursed_importing()
  app.run(debug=True, host="0.0.0.0")

@app.teardown_appcontext
def close_connection(_exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    main()
