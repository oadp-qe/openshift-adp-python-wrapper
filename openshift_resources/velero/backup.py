from ocp_resources.resource import NamespacedResource
import wrapper_constants.resources as r


class Backup(NamespacedResource):
    api_group = r.ApiGroups.VELERO_API_GROUP.value

