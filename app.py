from pathlib import Path
import importlib.util
import flask
import flask_restful

app = flask.Flask(__name__)
api = flask_restful.Api(app)

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

def cursed_importing():
        result = list(Path("routes/").rglob("*.py"))
    # print(result)
    for k in result:
        mod = import_path(k)
        mnice = {k:v for k, v in mod.__dict__.items() if k in methods}
        print(mnice)
        # print("handling " + mod.url)
        blank_class = type(mod.url, (flask_restful.Resource,), mnice )
        api.add_resource(blank_class, mod.url)
    


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
