import json

def show_versions():
    import mlflow
    #from databricks import sdk
    print("Versions:")
    print(f"   mlflow.version:",mlflow.__version__)
    #print(f"   sdk.version: {sdk.version.__version__}")


def dump_obj(obj, msg):
    print(f"{msg}:")
    for k,v in obj.__dict__.items():
        print(f"  {k}: {v}")


def dict_to_json(dct):
    return json.dumps(json.dumps(dct))


def dump_as_json(dct, title=None, sort_keys=None):
    if title:
        print(f"{title}:")
    print(json.dumps(dct, sort_keys=sort_keys, indent=2))


def write_as_json(path, dct):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(dct, sort_keys=True, indent=2))
