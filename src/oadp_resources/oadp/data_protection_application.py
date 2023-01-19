import logging

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from enum import Enum

from utils.common import wait_for

logger = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value


    class Condition(Enum):
        class Status(Enum):
            TRUE = "True"
            FALSE = "False"
            NONE = "None"

        class Type(Enum):
            RECONCILED = "Reconciled"

    def reconciled(self):
        try:
            manifest = self.instance
        except Exception as e:
            print(f'An error occurred: {e}')
        return any(
            co.type == self.Condition.Type.value.RECONCILED.value and
            co.status == self.Condition.Status.value.TRUE.value
            for co in manifest.status.conditions
        )

    def wait_for_success(self):
        return wait_for(
            condition_function=self.reconciled,
            description=f"DPA condition status is {self.Condition.Status.value.TRUE.value} and condition "
                        f"type is {self.Condition.Type.value.RECONCILED.value}, {self.name}",
            sleep=2,
            wait_timeout=240
        )
