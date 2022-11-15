from typing import List, Optional

from pydantic import BaseModel, Field
from resources.io.k8s.api.core import v1 as corev1
from resources.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from openshift_resources.resource import BaseResource
from wrapper_constants.oadp.datamover.volume_snapshot_backup import VolumeSnapshotBackupPhase
from wrapper_constants.resources import ApiGroups


class PVCData(BaseModel):
    name: Optional[str] = Field(None, description='name of the PersistentVolumeClaim')
    size: Optional[str] = Field(None, description='size of the PersistentVolumeClaim')
    storageClassName: Optional[str] = Field(
        None, description='name of the StorageClass'
    )


class VolumeSnapshotBackupSpec (BaseModel):
    protectedNamespace: Optional[str] = Field(
        None, description='Namespace where the Velero deployment is present'
    )
    resticSecretRef: Optional[corev1.LocalObjectReference] = Field(
        None, description='Restic Secret reference for given BSL'
    )
    volumeSnapshotContent: Optional[corev1.ObjectReference] = Field(
        None,
        description='ObjectReference contains enough information to let you inspect or modify the referred object. --- New uses of this type are discouraged because of difficulty describing its usage when embedded in APIs. 1. Ignored fields.  It includes many fields which are not generally honored.  For instance, ResourceVersion and FieldPath are both very rarely valid in actual usage. 2. Invalid usage help.  It is impossible to add specific help for individual usage.  In most embedded usages, there are particular restrictions like, "must refer only to types A and B" or "UID not honored" or "name must be restricted". Those cannot be well described when embedded. 3. Inconsistent validation.  Because the usages are different, the validation rules are different by usage, which makes it hard for users to predict what will happen. 4. The fields are both imprecise and overly precise.  Kind is not a precise mapping to a URL. This can produce ambiguity during interpretation and require a REST mapping.  In most cases, the dependency is on the group,resource tuple and the version of the actual struct is irrelevant. 5. We cannot easily change it.  Because this type is embedded in many locations, updates to this type will affect numerous schemas.  Don\'t make new APIs embed an underspecified API type they do not control. Instead of using this type, create a locally provided and used type that is well-focused on your reference. For example, ServiceReferences for admission registration: https://github.com/kubernetes/api/blob/release-1.17/admissionregistration/v1/types.go#L533 .',
    )


class VolumeSnapshotBackupStatus(BaseModel):
    completed: Optional[bool] = None
    conditions: Optional[List[metav1.Condition]] = Field(
        None,
        description='Include references to the volsync CRs and their state as they are running',
    )
    phase: Optional[VolumeSnapshotBackupPhase] = Field(None, description='volumesnapshot backup phase status')
    resticrepository: Optional[str] = Field(
        None, description='Includes restic repository path'
    )
    sourcePVCData: Optional[PVCData] = Field(
        None, description='Includes source PVC name and size'
    )
    volumeSnapshotClassName: Optional[str] = Field(
        None, description='name of the VolumeSnapshotClass'
    )


class VolumeSnapshotBackup(BaseResource):
    api_group : Optional[str] = Field(ApiGroups.DATAMOVER_OADP_API_GROUP.value, exclude=True, repr=False)

    spec: Optional[VolumeSnapshotBackupSpec ] = Field(
        None,
        description='VolumeSnapshotBackupSpec defines the desired state of VolumeSnapshotBackup',
    )
    status: Optional[VolumeSnapshotBackupStatus] = Field(
        None,
        description='VolumeSnapshotBackupStatus defines the observed state of VolumeSnapshotBackup',
    )


class VolumeSnapshotBackupList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description='APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources',
    )
    items: List[VolumeSnapshotBackup] = Field(
        ...,
        description='List of volumesnapshotbackups. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md',
    )
    kind: Optional[str] = Field(
        None,
        description='Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
    metadata: Optional[metav1.ListMeta] = Field(
        None,
        description='Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )

