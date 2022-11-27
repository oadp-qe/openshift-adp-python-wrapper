from ocp_resources.resource import NamespacedResource
from wrapper_constants.resources import ApiGroups


class BackupStorageLocation(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value
