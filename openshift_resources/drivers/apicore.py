from unittest.mock import MagicMock

from kubernetes.dynamic import DynamicClient
from kubernetes_pydantic.drivers.apicore import K8SCustomApiCore
from ocp_resources.resource import _get_api_version


class NewK8SCustomApiCore(K8SCustomApiCore):

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("config") and not isinstance(kwargs.get("config"), MagicMock):
            self.dyn_client = DynamicClient(self.api.client)
            self.version = _get_api_version(self.dyn_client, self.group, model)
