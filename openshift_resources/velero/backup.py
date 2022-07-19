from ocp_resources.resource import NamespacedResource
from constants.resources import VELERO_API_GROUP


class Backup(NamespacedResource):

    api_group = VELERO_API_GROUP

    def __init__(self,
                 hooks,
                 namespaces_to_include,
                 storage_location,
                 ):
        pass
