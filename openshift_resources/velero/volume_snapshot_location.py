from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from openshift_resources.resource import BaseResource
from wrapper_constants.resources import ApiGroups
from wrapper_constants.velero.volume_snapshot_location import VolumeSnapshotLocationPhase
from resources.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1


class VolumeSnapshotLocationStatus(BaseModel):
    phase: Optional[VolumeSnapshotLocationPhase] = Field(
        None,
        description='VolumeSnapshotLocationPhase is the lifecycle phase of a Velero VolumeSnapshotLocation.',
    )


class VolumeSnapshotLocationSpec(BaseModel):
    config: Optional[Dict[str, str]] = Field(
        None, description='Config is for provider-specific configuration fields.'
    )
    provider: str = Field(
        ..., description='Provider is the provider of the volume storage.'
    )


class VolumeSnapshotLocation(BaseResource):
    api_group: Optional[str] = Field(ApiGroups.VELERO_API_GROUP.value, exclude=True, repr=False)

    spec: Optional[VolumeSnapshotLocationSpec] = Field(
        None,
        description='VolumeSnapshotLocationSpec defines the specification for a Velero VolumeSnapshotLocation.',
    )
    status: Optional[VolumeSnapshotLocationStatus] = Field(
        None,
        description='VolumeSnapshotLocationStatus describes the current status of a Velero VolumeSnapshotLocation.',
    )


class VolumeSnapshotLocationList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description='APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources',
    )
    items: List[VolumeSnapshotLocation] = Field(
        ...,
        description='List of volumesnapshotlocations. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md',
    )
    kind: Optional[str] = Field(
        None,
        description='Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
    metadata: Optional[metav1.ListMeta] = Field(
        None,
        description='Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
