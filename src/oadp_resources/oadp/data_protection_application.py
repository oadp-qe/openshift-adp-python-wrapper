from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value
