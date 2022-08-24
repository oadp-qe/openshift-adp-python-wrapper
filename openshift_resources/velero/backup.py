from ocp_resources.resource import NamespacedResource
from constants.resources import VELERO_API_GROUP


class Backup(NamespacedResource):
    api_group = VELERO_API_GROUP
