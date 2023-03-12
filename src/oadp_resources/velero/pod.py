from enum import Enum
from ocp_resources.resource import NamespacedResource


class VeleroPod(NamespacedResource):
    api_version = NamespacedResource.ApiVersion.V1

    # BackupPhase is a str representation of the lifecycle phase
    # of a Velero backup.
    class Label(Enum):
        KEY = "component"
        VALUE = "velero"
