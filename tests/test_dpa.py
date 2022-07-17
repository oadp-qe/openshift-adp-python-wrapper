import kubernetes

from openshift.dynamic import DynamicClient
from openshift_resources.data_protection_application import DataProtectionApplication


class DynamicClient:
    pass


def oadp_ocp_client():
    yield  DynamicClient(client=kubernetes.config.new_client_from_config())


def test_dpa(oadp_ocp_client):
    with DataProtectionApplication() as dpa:
        dpa.wait_for_reconciliation()
        pass
