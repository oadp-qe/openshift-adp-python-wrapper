import logging

from ocp_resources.resource import NamespacedResource

from constants.common import FOUR_MINUTES
from constants.resources import OADP_API_GROUP

LOGGER = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = OADP_API_GROUP

    def __init__(self,
        name,
        namespace,
        client=None,
        teardown=True,
        timeout=FOUR_MINUTES,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=None,
        **kwargs):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            timeout=timeout,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )

    def wait_for_reconciliation(self):
        LOGGER.info(f"[DUMMY]waiting for {self.name} reconciliation")


