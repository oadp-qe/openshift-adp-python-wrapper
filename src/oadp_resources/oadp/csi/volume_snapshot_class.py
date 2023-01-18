from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from enum import Enum


class VolumeSnapshotClass(NamespacedResource):
    api_group = ApiGroups.VOLUME_SNAPSHOT_CLASS.value

    class Platform(Enum):
        class AWS(Enum):
            PROVIDER = "aws"
            DRIVER = "ebs.csi.aws.com"

        class GCP(Enum):
            PROVIDER = "gcp"
            DRIVER = "pd.csi.storage.gke.io"

        class AZURE(Enum):
            PROVIDER = "azure"
            DRIVER = "disk.csi.azure.com"

        class OSP(Enum):
            PROVIDER = "osp"
            DRIVER = "openshift-storage.rbd.csi.ceph.com"

        class IBM(Enum):
            PROVIDER = "osp"
            DRIVER = "openshift-storage.cephfs.csi.ceph.com"

    @classmethod
    def get_csi_driver_by_provider(cls, provider):
        if provider == cls.Platform.AWS.value.PROVIDER.value:
            return cls.Platform.AWS.value.DRIVER.value
        elif provider == cls.Platform.GCP.value.PROVIDER.value:
            return cls.Platform.GCP.value.DRIVER.value
        elif provider == cls.Platform.AZURE.value.PROVIDER.value:
            return cls.Platform.AZURE.value.DRIVER.value
        elif provider == cls.Platform.OSP.value.PROVIDER.value:
            return cls.Platform.OSP.value.DRIVER.value
        elif provider == cls.Platform.IBM.value.PROVIDER.value:
            return cls.Platform.IBM.value.DRIVER.value
