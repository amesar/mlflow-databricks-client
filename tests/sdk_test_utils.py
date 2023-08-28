from mlflow_databricks_client.common.utils import dump_as_json


def dump_rsp(rsp, title=None, show_response_as_json=False):
    dct = rsp.as_dict()
    if show_response_as_json:
        dump_as_json(dct, title)
    else:
        print()
        print("=================================================")
        print(f"| {title}")
        print("+=================================================")
        print(rsp)
    return dct

