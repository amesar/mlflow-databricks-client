import yaml
from mlflow_databricks_client.common.utils import dump_as_json

def read_config_file(path="config.yaml"):
    with open(path,  encoding="utf-8") as f:
        dct = yaml.safe_load(f)
        print(f"Config for '{path}':")
        for k,v in dct.items():
            print(f"  {k}: {v}")
    return dct


def _check_object_id(object_id, perms):
    _object_id = perms.get("object_id")
    _object_id = _object_id.split("/")[2]
    assert _object_id == object_id


cfg = read_config_file()
dump_as_json(cfg, "Test Config")
