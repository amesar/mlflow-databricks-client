from mlflow_databricks_client.common.utils import dump_as_json


def dump_rsp(rsp, title=None, show_response_as_json=False):
    if show_response_as_json:
        try:
            dct = rsp.as_dict()
            dump_as_json(dct, title)
            return dct
        except Exception: # AttributeError
            print("WARNING: rsp.as_dict() failed for type '}type(rsp)}")
            dump_sdk_obk(rsp, title)
    else:
        dump_sdk_obk(rsp, title)
    return None


def dump_sdk_obk(obj, title):
    print()
    print("=================================================")
    print(f"| {title}")
    print("+=================================================")
    print(obj)

