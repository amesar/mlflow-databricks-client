import yaml
from mlflow_databricks_client.common.utils import dump_as_json

def read_config_file(path="config.yaml"):
    with open(path,  encoding="utf-8") as f:
        dct = yaml.safe_load(f)
        print(f"Config for '{path}':")
        for k,v in dct.items():
            print(f"  {k}: {v}")
    return dct


def check_object_id(object_id, perms):
    _object_id = perms.get("object_id")
    _object_id = _object_id.split("/")[2]
    assert _object_id == object_id


def do_test_get_registered_model_permissions(perms):
    assert perms.get("object_type") == "registered-model"
    acl = perms.get("access_control_list")
    assert acl
    assert len(acl) > 0

def do_test_get_experiment_permission_levels(perms):
    perms = perms.get("permission_levels")
    assert perms
    assert len(perms) > 0
    matches = [ p for p in perms if p["permission_level"] == "CAN_READ" ]
    assert len(matches) == 1


def func_name():
    import inspect
    return inspect.stack()[1][3]


cfg = read_config_file()
dump_as_json(cfg, "Test Config")
