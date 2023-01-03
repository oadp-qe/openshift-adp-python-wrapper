from ocp_resources.constants import TIMEOUT_4MINUTES

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value

    @classmethod
    def delete_all(cls, wait=False, timeout=TIMEOUT_4MINUTES):
        """
        Delete all DPA CRs
        @param wait: wait till the resource is deleted
        @param timeout: Time to wait for the resource.
        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        all_dpas : list[cls] = list(cls.get())
        for dpa in all_dpas:
            dpa.delete(wait, timeout)
