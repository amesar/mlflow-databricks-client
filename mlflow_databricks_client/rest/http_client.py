import json, os
import requests
from mlflow.utils.databricks_utils import get_databricks_host_creds


_TIMEOUT = 15

class HttpClient():
    def __init__(self, api_prefix="api/2.0"):
        self.creds = get_databricks_host_creds()
        self.api_uri = os.path.join(self.creds.host, api_prefix)
        self.headers ={ "Authorization": f"Bearer {self.creds.token}" }


    def get(self, resource, params=None):
        uri = self._mk_uri(resource)
        rsp = requests.get(uri, headers=self.headers, json=params, timeout=_TIMEOUT)
        self._check_response(rsp, params)
        return rsp.json()


    def post(self, resource, data=None):
        return self._mutate(requests.post, resource, data)


    def put(self, resource, data=None):
        return self._mutate(requests.put, resource, data)


    def patch(self, resource, data=None):
        return self._mutate(requests.patch, resource, data)


    def delete(self, resource, data=None):
        return self._mutate(requests.delete, resource, data)


    def _mutate(self, method, resource, data=None):
        uri = self._mk_uri(resource)
        data = self._json_dumps(data)
        rsp = method(uri, headers=self.headers, data=data, timeout=_TIMEOUT)
        self._check_response(rsp, data)
        return rsp.json()


    def _json_dumps(self, data):
        return json.dumps(data) if data else None

    def _check_response(self, rsp, params=None):
        from requests.exceptions import HTTPError
        if rsp.status_code < 200 or rsp.status_code > 299:
            msg = { "http_status_code": rsp.status_code, "uri": rsp.url, "method": rsp.request.method, "params": params, "response": rsp.text }
            raise HTTPError(json.dumps(msg))
        return rsp

    def _mk_uri(self, resource):
        return f"{self.api_uri}/{resource}"

    def __repr__(self):
        return self.api_uri
