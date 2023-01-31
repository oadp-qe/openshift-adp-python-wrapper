from oadp_constants.resources import ApiGroups
from ocp_resources.resource import Resource
from enum import Enum


class VolumeSnapshotClass(Resource):
    api_group = ApiGroups.VOLUME_SNAPSHOT_CLASS.value

    class Platform(Enum):
        class Aws(Enum):
            Provider = "aws"
            Driver = "ebs.csi.aws.com"

        class Gcp(Enum):
            Provider = "gcp"
            Driver = "pd.csi.storage.gke.io"

        class Azure(Enum):
            Provider = "azure"
            Driver = "disk.csi.azure.com"

        class Osp(Enum):
            Provider = "osp"
            Driver = "openshift-storage.rbd.csi.ceph.com"

        class Ibm(Enum):
            Provider = "osp"
            Driver = "openshift-storage.cephfs.csi.ceph.com"

    @classmethod
    def get_csi_driver_by_provider(cls, provider):
        if provider == cls.Platform.Aws.value.Provider.value:
            return cls.Platform.Aws.value.Driver.value
        elif provider == cls.Platform.Gcp.value.Provider.value:
            return cls.Platform.Gcp.value.Driver.value
        elif provider == cls.Platform.Azure.value.Provider.value:
            return cls.Platform.Azure.value.Driver.value
        elif provider == cls.Platform.Osp.value.Provider.value:
            return cls.Platform.Osp.value.Driver.value
        elif provider == cls.Platform.Ibm.value.Provider.value:
            return cls.Platform.Ibm.value.Driver.value
