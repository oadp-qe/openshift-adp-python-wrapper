from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value
