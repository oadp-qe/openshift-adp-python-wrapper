from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):

    api_group = "oadp.openshift.io"

    def __init__(self,
                 hooks,
                 namespaces_to_include,
                 storage_location,
                 ):
        pass
