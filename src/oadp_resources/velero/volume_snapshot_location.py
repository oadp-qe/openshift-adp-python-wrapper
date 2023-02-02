from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups


class VolumeSnapshotLocation(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    class VolumeSnapshotLocationPhase(Enum):
        AVAILABLE = 'Available'
        UNAVAILABLE = 'Unavailable'
