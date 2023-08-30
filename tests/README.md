
## Tests - mlflow-databricks-client 

### Overview
* Tests for the Databricks-specific MLflow REST and SDK clients.
* We simply test that the API call is executed properly.
* The tests are verbose in that they display the JSON response payload for API calls.

### Steps

* `pip install -e ..[tests] --upgrade`
* Copy [config.yaml.template](config.yaml.template]) to `config.yaml`.
* Make appropriate changes for your Databricks workspace.
* `pytest -s -v test*.py`

### Tests

#### REST client tests
* [test_rest_experiment_permissions.py](test_rest_experiment_permissions.py)
* [test_rest_model_permissions.py](test_rest_model_permissions.py)
* [test_rest_runs.py](test_rest_runs.py)
* [test_rest_uc_model_permissions.py](test_rest_uc_model_permissions.py)
* [test_rest_uc_oss.py](test_rest_uc_oss.py)

#### SDK client tests
* [test_sdk_experiment_permissions.py](test_sdk_experiment_permissions.py)
* [test_sdk_model_permissions.py](test_sdk_model_permissions.py)
* [test_sdk_runs.py](test_sdk_runs.py)
* [test_sdk_uc_model_permissions.py](test_sdk_uc_model_permissions.py)
