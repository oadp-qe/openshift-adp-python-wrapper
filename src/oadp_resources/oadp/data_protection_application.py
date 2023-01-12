from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from enum import Enum


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


