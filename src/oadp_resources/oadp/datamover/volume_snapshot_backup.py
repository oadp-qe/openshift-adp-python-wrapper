from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups


class VolumeSnapshotLocation(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

