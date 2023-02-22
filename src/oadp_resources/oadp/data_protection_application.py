import logging

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from enum import Enum

from oadp_utils.wait import wait_for

from oadp_utils.phase import log_status

logger = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value

    class DataProtectionApplicationCondition(Enum):
        class Status(Enum):
            TRUE = "True"
            FALSE = "False"
            NONE = "None"

        class Type(Enum):
            RECONCILED = "Reconciled"

    def reconciled(self):
        try:
            instance = self.instance
            log_status(self)
            return any(
                co.type == self.DataProtectionApplicationCondition.Type.value.RECONCILED.value and
                co.status == self.DataProtectionApplicationCondition.Status.value.TRUE.value
                for co in instance.status.conditions
            )
        except AttributeError:
            return False

    def wait_for_reconciled(self, wait_timeout=240, sleep=5):
        return wait_for(
            condition_function=self.reconciled,
            description=f"DPA condition status to be {self.DataProtectionApplicationCondition.Status.value.TRUE.value} and condition "
                        f"type to be {self.DataProtectionApplicationCondition.Type.value.RECONCILED.value}, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )
