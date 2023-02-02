from oadp_constants.resources import ApiGroups
from ocp_resources.resource import Resource
from enum import Enum


class VolumeSnapshotClass(Resource):
    api_group = ApiGroups.VOLUME_SNAPSHOT_CLASS.value

    class Platform(Enum):
        class Aws(Enum):
            PROVIDER = "aws"
            DRIVER = "ebs.csi.aws.com"

        class Gcp(Enum):
            PROVIDER = "gcp"
            DRIVER = "pd.csi.storage.gke.io"

        class Azure(Enum):
            PROVIDER = "azure"
            DRIVER = "disk.csi.azure.com"

        class Osp(Enum):
            PROVIDER = "osp"
            DRIVER = "openshift-storage.rbd.csi.ceph.com"

        class Ibm(Enum):
            PROVIDER = "osp"
            DRIVER = "openshift-storage.cephfs.csi.ceph.com"

    @classmethod
    def get_csi_driver_by_provider(cls, provider):
        if provider == cls.Platform.Aws.value.PROVIDER.value:
            return cls.Platform.Aws.value.DRIVER.value
        elif provider == cls.Platform.Gcp.value.PROVIDER.value:
            return cls.Platform.Gcp.value.DRIVER.value
        elif provider == cls.Platform.Azure.value.PROVIDER.value:
            return cls.Platform.Azure.value.DRIVER.value
        elif provider == cls.Platform.Osp.value.PROVIDER.value:
            return cls.Platform.Osp.value.DRIVER.value
        elif provider == cls.Platform.Ibm.value.PROVIDER.value:
            return cls.Platform.Ibm.value.DRIVER.value
