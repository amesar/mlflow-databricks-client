import time
from mlflow_databricks_client.rest.client import DatabricksUcMlflowClient
from . common_test import cfg
from mlflow_databricks_client.common.utils import dump_as_json

client = DatabricksUcMlflowClient()

model_name = cfg["unity_catalog_registry"]["model"]
principal = cfg["principal"]

model_name_tmp = f"{model_name}_tmp"
create_model_version_sleep = 3


# ==== Test Registered Model

def test_get_registered_model():
    rsp = client.get_registered_model(model_name)
    dump_as_json(rsp, "test_get_registered_model")
    model = rsp["registered_model"]
    assert model["name"] == model_name

def test_create_registered_model():
    _delete_registered_model(model_name_tmp)

    #rsp = client.create_registered_model(model_name_tmp)
    #rsp = client.create_registered_model(model_name_tmp, description="Hi there")
    #tags = {"name": "Panthera uncia"}
    tags = [ { "key": "name", "value": "Panthera uncia"} ]
    rsp = client.create_registered_model(model_name_tmp, description="Cool cat", tags=tags)
    dump_as_json(rsp, "test_create_registered_model.create")

    rsp = client.get_registered_model(model_name_tmp)
    dump_as_json(rsp, "test_create_registered_model.get")

    client.delete_registered_model(model_name_tmp)

def test_update_registered_model():
    rsp = client.update_registered_model(model_name, "My new description")
    dump_as_json(rsp, "test_update_registered_model.update")

    #rsp = client.update_registered_model(model_name) 
    # NOTE: though doc says description is optional, error is returned not specified
    # ERROR: { error_code: "INVALID_PARAMETER_VALUE","message":"UpdateRegisteredModel Nothing to update" }


def test_search_registered_models():
    rsp = client.search_registered_models()
    dump_as_json(rsp, "test_search_registered_models.search")

def test_search_registered_models_with_filter():
    rsp = client.search_registered_models(filter=f"name='{model_name}'")
    dump_as_json(rsp, "test_search_registered_models_with_filter")


# ==== Test Model Versions

_model_version = None
_run_id = None
_source = None

def skip_test_search_model_versions():
    # NOTE: Per MLflow doc, filter is optional but Databricks requires it (no documentation).
    # ERROR: { "error_code":"INVALID_PARAMETER_VALUE","message":"Missing filter: please specify a filter parameter in the format `name = 'model_name'`."}"}
    rsp = client.search_model_versions()
    dump_as_json(rsp, "test_search_model_versions.search")

def test_search_model_versions_with_filter():
    global _model_version, _run_id, _source
    rsp = client.search_model_versions(filter=f"name='{model_name}'")
    dump_as_json(rsp, "test_search_model_versions_with_filter")

    model_versions = rsp["model_versions"]
    _model_version = model_versions[0]["version"] # NOTE: used by subsequent tests below
    _run_id = model_versions[0]["run_id"] 
    _source = model_versions[0]["source"] 

def test_create_model_version():
    rsp = client.create_model_version(model_name, _source, _run_id, description="Test version")
    dump_as_json(rsp, "test_create_model_version.create")
    vr = rsp["model_version"]
    print("New model_version:", vr["version"])
    time.sleep(create_model_version_sleep) 

    rsp = client.get_model_version(model_name, vr["version"])
    dump_as_json(rsp, "test_create_model_version.get")

    client.delete_model_version(model_name, vr["version"])
    dump_as_json(rsp, "test_create_model_version.delete")

def test_get_model_version():
    rsp = client.get_model_version(model_name, _model_version)
    dump_as_json(rsp, "test_get_model_version")

def test_update_model_version():
    rsp = client.update_model_version(model_name, _model_version, "My description")
    dump_as_json(rsp, "test_update_model_version")

def test_set_model_version_tag():
    rsp = client.set_model_version_tag(model_name, _model_version, "my_key", "my_value")
    dump_as_json(rsp, "test_set_model_version_tag")
    rsp = client.get_model_version(model_name, _model_version) 
    dump_as_json(rsp, "test_set_model_version_tag_with_stage.get")

def test_set_model_version_tag_with_stage():
    rsp = client.set_model_version_tag(model_name, _model_version, "my_key", "my_value", "production") 
    dump_as_json(rsp, "test_set_model_version_tag_with_stage")
    rsp = client.get_model_version(model_name, _model_version) # NOTE: stage is ignored
    dump_as_json(rsp, "test_set_model_version_tage_with_stage.get")

def skip_test_set_model_version_tag_with_no_tag():
    rsp = client.set_model_version_tag(model_name, _model_version)
    dump_as_json(rsp, "test_set_model_version_tag_with_no_tag")
    # NOTE: MLflow Python doc strangely says key and value are optional i
    # ERROR: "{g"error_code":"INVALID_PARAMETER_VALUE","message":"Tag name  is not valid","details":[{"@type":"type.googleapis.com/google.rpc.RequestInfo","request_id":"85d1bcc6-ae37-4afb-b8b6-f9da7c612d13","serving_data":""}]}"}


# ==== Test model alias

_alias = "test_champ"

def test_registered_model_alias():
    rsp = client.set_registered_model_alias(model_name, _alias, _model_version)
    dump_as_json(rsp, "test_registered_model_alias.set")

    rsp = client.get_registered_model_by_alias(model_name, _alias)
    dump_as_json(rsp, "test_registered_model_alias.get")

    rsp = client.delete_registered_model_alias(model_name, _alias, _model_version)
    dump_as_json(rsp, "test_registered_model_alias.delete")

    rsp = client.get_model_version(model_name, _model_version)
    dump_as_json(rsp, "test_registered_model_alias.get_after_delete")


# ==== Helper

def _delete_registered_model(model_name):
    import requests
    try:
        client.delete_registered_model(model_name)
    except requests.exceptions.HTTPError:
        pass
