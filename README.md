# Databricks MLflow API Client

Provides two shim-like client wrappers for the Databricks-specific MLflow REST API and the Databricks SDK.

The two shim clients are:
  * [REST client](out/rest/client.html) - directly calls the REST API and returns the actual API JSON payloads
  * [SDK client](out/sdk/client.html) - pass-through to the Databricks SDK just for MLflow Databricks-specific methods

## MLflow API Documentation

### Open Source MLflow API

* [Python API](https://www.mlflow.org/docs/latest/python_api/index.html) 
* [REST API](https://www.mlflow.org/docs/latest/rest-api.html)
* [Data Structures](https://www.mlflow.org/docs/latest/rest-api.html#data-structures)

### Databricks MLflow API

#### REST API

* Machine Learning
  * [Experiments](https://docs.databricks.com/api/workspace/experiments)
  * [Model Registry](https://docs.databricks.com/api/workspace/modelregistry)
* Unity Catalog
  * [Grants aka Permissions](https://docs.databricks.com/api/workspace/grants)

#### [Python API (SDK)](https://databricks-sdk-py.readthedocs.io/en/latest/index.html)
* [Machine Learning](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/workspace-ml.html)
  * [Experiments](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html)
  * [Model Registry](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html)
* [Unity Catalog](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/workspace-catalog.html)
  * [Grants aka Permissions](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html)

## Databricks-specific  MLflow REST API Endpoints

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


### REST API Usage

#### Source code

  * Client definition: [mlflow_databricks_client/rest/client.py](mlflow_databricks_client/rest/client.py)
  * Examples - [tests](tests):
    * [test_rest_model_permissions.py](tests/test_rest_model_permissions.py)
    * [test_rest_experiment_permissions.py](tests/test_rest_experiment_permissions.py)
    * [test_rest_uc_model_permissions.py](tests/test_rest_uc_model_permissions.py)
    * [test_rest_uc_oss.py](tests/test_rest_uc_oss.py)

#### Credentials

See [Access the MLflow tracking server from outside Databricks](https://docs.databricks.com/en/mlflow/access-hosted-tracking-server.html).

By default the Databricks credentials will be picked up from the default profile in `$HOME/.databricks.cfg`.

To point to another workspace:
```
export DATABRICKS_HOST=https://mycompany.my-workspace.com
export DATABRICKS_TOKEN=MY_TOKEM
```
#### Example
```
from databricks_mlflow_client.rest.client import DatabricksMlflowClient
client = DatabricksMlflowClient()
model = client.get_experiment_permissions("Sklearn_Wine_best")
print(model)
```

```
{
  "access_control_list": [
    {
      "all_permissions": [
        {
          "inherited": true,
          "inherited_from_object": [
            "/directories/767933989557963"
          ],
          "permission_level": "CAN_MANAGE"
        }
      ],
      "display_name": "Andre API",
      "user_name": "andre@mycompany.com"
    },
 . . .
}
```

###  SDK API Usage

#### Source code

  * Client definition: [mlflow_databricks_client/sdk/client.py](mlflow_databricks_client/sdk/client.py)
  * Examples - [tests](tests):
    * [test_sdk_experiment_permissions.py](tests/test_sdk_experiment_permissions.py)

#### Example
```
from databricks_mlflow_client.sdk.client import DatabricksMlflowClient
client = DatabricksMlflowClient()
model = client.get_experiment_permissions("Sklearn_Wine_best")
print(model)
```

```
ObjectPermissions(access_control_list=[AccessControlResponse(all_permissions=[Permission(inherited=True, inherited_from_object=['/directories/767933989557963'], permission_level=<PermissionLevel.CAN_MANAGE: 'CAN_MANAGE'>)], display_name='Andre API', group_name=None, service_principal_name=None, user_name='andre@mycompany.com'), AccessControlResponse(all_permissions=[Permission(inherited=True, inherited_from_object=['/directories/'], permission_level=<PermissionLevel.CAN_MANAGE: 'CAN_MANAGE'>)], display_name='root-service-principal-e2-demo-west-ws-do-not-delete', group_name=None, service_principal_name='091812d4-z5ec-4544-b6zf-64135891fee1', user_name=None), AccessControlResponse(all_permissions=[Permission(inherited=False, inherited_from_object=None, permission_level=<PermissionLevel.CAN_READ: 'CAN_READ'>)], display_name=None, group_name='users', service_principal_name=None, user_name=None), AccessControlResponse(all_permissions=[Permission(inherited=True, inherited_from_object=['/directories/'], permission_level=<PermissionLevel.CAN_MANAGE: 'CAN_MANAGE'>)], display_name=None, group_name='admins', service_principal_name=None, user_name=None)], object_id='/experiments/2668333326915655', object_type='mlflowExperiment')
```
