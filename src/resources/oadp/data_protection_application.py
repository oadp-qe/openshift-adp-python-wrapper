from ocp_resources.resource import NamespacedResource
from wrapper_constants.resources import ApiGroups


class DataProtectionApplication(NamespacedResource):
    api_group = ApiGroups.OADP_API_GROUP.value
