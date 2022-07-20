from ocp_resources.resource import NamespacedResource

import openshift_resources.constants


class Backup(NamespacedResource):

    api_group = openshift_resources.constants.VELERO_API_GROP
