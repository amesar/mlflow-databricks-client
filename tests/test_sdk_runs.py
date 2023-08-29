from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
from . sdk_test_utils import dump_rsp
from . common_test import func_name, cfg
client = DatabricksMlflowClient()

experiment_name = cfg["experiment"]
experiment_id = client._get_experiment_id(experiment_name)

def test_delete_runs():
    max_timestamp_millis = 123
    max_runs = None
    rsp = client.delete_runs(experiment_id, max_timestamp_millis, max_runs)
    dump_rsp(rsp, func_name(), True)


def test_restore_runs():
    min_timestamp_millis = 123
    max_runs = None
    rsp = client.restore_runs(experiment_id, min_timestamp_millis, max_runs)
    dump_rsp(rsp, func_name(), True)

