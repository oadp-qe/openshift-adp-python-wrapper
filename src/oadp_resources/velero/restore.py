from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups


class Restore(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value
