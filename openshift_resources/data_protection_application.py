import logging

from ocp_resources.resource import NamespacedResource

LOGGER = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = "oadp.openshift.io"

    def __init__(self):
        pass

    def wait_for_reconciliation(self):
        LOGGER.info(f"[DUMMY]waiting for {self.name} reconciliation")


