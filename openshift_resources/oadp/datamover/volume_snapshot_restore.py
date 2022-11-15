from typing import List, Optional

from pydantic import BaseModel, Field
from resources.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1
from resources.io.k8s.api.core import v1 as corev1

from wrapper_constants.oadp.datamover.volume_snapshot_restore import VolumeSnapshotRestorePhase
from wrapper_constants.resources import ApiGroups

from .volume_snapshot_backup import PVCData
from ...resource import BaseResource


class VSBRef(BaseModel):
    resticrepository: Optional[corev1.LocalObjectReference] = Field(
        None, description='Includes restic repository path'
    )
    sourcePVCData: Optional[PVCData] = Field(
        None, description='Includes backed up PVC name and size'
    )
    volumeSnapshotClassName: Optional[str] = Field(
        None, description='name of the VolumeSnapshotClass'
    )


class VolumeSnapshotRestoreSpec(BaseModel):
    protectedNamespace: Optional[str] = Field(
        None, description='Namespace where the Velero deployment is present'
    )
    resticSecretRef: Optional[corev1.LocalObjectReference] = Field(
        None,
        description='LocalObjectReference contains enough information to let you locate the referenced object inside the same namespace.',
    )
    volumeSnapshotMoverBackupRef: Optional[VSBRef] = Field(
        None, description='Includes associated volumesnapshotbackup details'
    )


class VolumeSnapshotRestoreStatus(BaseModel):
    conditions: Optional[List[metav1.Condition]] = None
    phase: Optional[VolumeSnapshotRestorePhase] = Field(
        None, description='volumesnapshot restore phase status'
    )
    snapshotHandle: Optional[str] = None


class VolumeSnapshotRestore(BaseResource):
    api_group: Optional[str] = Field(ApiGroups.DATAMOVER_OADP_API_GROUP.value, exclude=True, repr=False)

    spec: Optional[VolumeSnapshotRestoreSpec] = Field(
        None,
        description='VolumeSnapshotRestoreSpec defines the desired state of VolumeSnapshotRestore',
    )
    status: Optional[VolumeSnapshotRestoreStatus] = Field(
        None,
        description='VolumeSnapshotRestoreStatus defines the observed state of VolumeSnapshotRestore',
    )


class VolumeSnapshotRestoreList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description='APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources',
    )
    items: List[VolumeSnapshotRestore] = Field(
        ...,
        description='List of volumesnapshotrestores. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md',
    )
    kind: Optional[str] = Field(
        None,
        description='Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
    metadata: Optional[metav1.ListMeta] = Field(
        None,
        description='Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )

