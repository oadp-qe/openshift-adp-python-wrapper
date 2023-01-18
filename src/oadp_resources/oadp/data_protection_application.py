import logging

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value

    def reconciled(self):
        logger.info(self.instance.status.conditions)
        if self.instance and self.instance.status and self.instance.status.conditions:
            return [co for co in self.instance.status.conditions if co.type == "Reconciled" and co.status]
