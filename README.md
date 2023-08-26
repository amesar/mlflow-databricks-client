# Databricks MLflow API Client - WIP

Python client for Databricks-specific MLflow REST API endpoints.

## Release Notes

Only the registered model and experiment get permission endpoints have been implemented.

## MLflow API Documentation

* [Python API](https://www.mlflow.org/docs/latest/python_api/index.html) 
* [REST API](https://www.mlflow.org/docs/latest/rest-api.html)
* [Data Structures](https://www.mlflow.org/docs/latest/rest-api.html#data-structures)

## Databricks-specific  MLflow API documentation

Databricks-specific resources (endpoints) do not have consistent naming so it is hard at first glance to tell which MLflow resources
are open source and which ones are Databricks-specific.

Naming patterns for Databricks-specific MLflow resource fall into three categories:
* Start with `mlflow/databricks` (good).
  * Example: `/2.0/mlflow/databricks/registered-models/get` 
* Start with `mlflow` but with no indication they are Databricks-specific (not so good).
  * Example: `/2.0/mlflow/transition-requests/create`
* Have no mention of mlflow (even less good).
  * Example: `/2.0/permissions/registered-models/{model_id}`

### REST API

| Method | Resource |
|-----|-------|
| | **_Registered Models_** |
| GET | [/api/2.0/mlflow/databricks/registered-models/get](https://docs.databricks.com/api/workspace/modelregistry/getmodel) |
| | **_Registered Model Permissions_** |
| GET | [/api/2.0/permissions/registered-models/{model_id}](https://docs.databricks.com/api/workspace/modelregistry/getmodel)   |
| PUT | [/api/2.0/permissions/registered-models/{model_id}](https://docs.databricks.com/api/workspace/modelregistry/setregisteredmodelpermissions) |
| PATCH | [/api/2.0/permissions/registered-models/{model_id}](https://docs.databricks.com/api/workspace/modelregistry/updateregisteredmodelpermissions) |
| GET | [/api/2.0/permissions/registered-models/{model_id}/permissionLevels](https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissionlevels) |
| | **_Experiment Permissions_** |
| GET | [/api/2.0/permissions/experiments/{experiment_id}](https://docs.databricks.com/api/workspace/experiments/getexperimentpermissions) |
| PUT | [/api/2.0/permissions/experiments/{experiment_id}](https://docs.databricks.com/api/workspace/experiments/setexperimentpermissions) |
| PATCH | [/api/2.0/permissions/experiments/{experiment_id}](https://docs.databricks.com/api/workspace/experiments/updateexperimentpermissions) |
| GET | [/api/2.0/permissions/experiments/{experiment_id}/permissionLevels](https://docs.databricks.com/api/workspace/experiments/getexperimentpermissionlevels) | 
| | **_Delete and Restore Runs_** |
| POST | [/api/2.0/mlflow/databricks/runs/delete-runs](https://docs.databricks.com/api/workspace/experiments/deleteruns) |
| POST | [/api/2.0/mlflow/databricks/runs/restore-runs](https://docs.databricks.com/api/workspace/experiments/restoreruns) |
| | **_Transition Requests_** |
| POST | [/api/2.0/mlflow/transition-requests/create](https://docs.databricks.com/api/workspace/modelregistry/createtransitionrequest) |
| GET | [/api/2.0/mlflow/transition-requests/list](https://docs.databricks.com/api/workspace/modelregistry/listtransitionrequests) |
| POST | [/api/2.0/mlflow/transition-requests/approve](https://docs.databricks.com/api/workspace/modelregistry/approvetransitionrequest) |
| POST |  [/api/2.0/mlflow/transition-requests/reject](https://docs.databricks.com/api/workspace/modelregistry/rejecttransitionrequest) |
| DELETE |  [/api/2.0/mlflow/transition-requests/delete](https://docs.databricks.com/api/workspace/modelregistry/deletetransitionrequest) |
| | **_Model Version Comments_** | 
| POST | [/api/2.0/mlflow/comments/create](https://docs.databricks.com/api/workspace/modelregistry/createcomment) |
| PATCH | [/api/2.0/mlflow/comments/update](https://docs.databricks.com/api/workspace/modelregistry/updatecomment) |
| DELETE | [/api/2.0/mlflow/comments/delete](https://docs.databricks.com/api/workspace/modelregistry/deletecomment) |
| | **_Webhooks_** | 
| POST | [/api/2.0/mlflow/registry-webhooks/create](https://docs.databricks.com/api/workspace/modelregistry/createwebhook) |
| GET | [/api/2.0/mlflow/registry-webhooks/list](https://docs.databricks.com/api/workspace/modelregistry/listwebhooks) |
| PATCH | [/api/2.0/mlflow/registry-webhooks/update](https://docs.databricks.com/api/workspace/modelregistry/updatewebhook) |
| DELETE | [/api/2.0/mlflow/registry-webhooks](https://docs.databricks.com/api/workspace/modelregistry/deletewebhook) |
| POST | [/api/2.0/mlflow/registry-webhooks/test](https://docs.databricks.com/api/workspace/modelregistry/testregistrywebhook) |

## Usage

For details see [databricks_mlflow_client/rest/client.py](databricks_mlflow_client/rest/client.py).

### Credentials

See [Access the MLflow tracking server from outside Databricks](https://docs.databricks.com/en/mlflow/access-hosted-tracking-server.html).

By default the Databricks credentials will be picked up from the default profile in `$HOME/.databricks.cfg`.

To point to another workspace:
```
export DATABRICKS_HOST=https://mycompany.my-workspace.com
export DATABRICKS_TOKEN=MY_TOKEM
```
### Example
```
from databricks_mlflow_client.rest.client import DatabricksMlflowClient

client = DatabricksMlflowClient()
model = client.get_registered_model_databricks("Sklearn_Wine_best")
print(model)
```

```
{
  "registered_model_databricks": {
    "name": "Sklearn_Wine_best",
    "creation_timestamp": 1680931584248,
    "last_updated_timestamp": 1681435287008,
    "user_id": "andre@mycompany.com",
    "latest_versions": [
      {
        "name": "Sklearn_Wine_best",
        "version": "10",
        "creation_timestamp": 1681106535915,
    . . .
      }
    ],
    "id": "32aaa09aa75b42169eded072d87384ae",
    "permission_level": "CAN_MANAGE"
  }
}
```
