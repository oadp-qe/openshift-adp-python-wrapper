from typing import List, Optional

from pydantic import BaseModel, Field
from resources.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

from openshift_resources.resource import BaseResource
from openshift_resources.velero.backup import BackupSpec
from wrapper_constants.resources import ApiGroups
from wrapper_constants.velero.schedule import SchedulePhase


class ScheduleStatus(BaseModel):
    lastBackup: Optional[str] = Field(
        None,
        description='LastBackup is the last time a Backup was run for this Schedule schedule',
    )
    phase: Optional[SchedulePhase] = Field(
        None, description='Phase is the current phase of the Schedule'
    )
    validationErrors: Optional[List[str]] = Field(
        None,
        description='ValidationErrors is a slice of all validation errors (if applicable)',
    )


class ScheduleSpec(BaseModel):
    schedule: str = Field(
        ...,
        description='Schedule is a Cron expression defining when to run the Backup.',
    )
    template: BackupSpec = Field(
        ...,
        description='Template is the definition of the Backup to be run on the provided schedule',
    )
    useOwnerReferencesInBackup: Optional[bool] = Field(
        None,
        description='UseOwnerReferencesBackup specifies whether to use OwnerReferences on backups created by this Schedule.',
    )


class Schedule(BaseResource):
    api_group : Optional[str] = Field(ApiGroups.VELERO_API_GROUP.value, exclude=True, repr=False)
    spec: Optional[ScheduleSpec] = Field(
        None, description='ScheduleSpec defines the specification for a Velero schedule'
    )
    status: Optional[ScheduleStatus] = Field(
        None,
        description='ScheduleStatus captures the current state of a Velero schedule',
    )


class ScheduleList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description='APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources',
    )
    items: List[Schedule] = Field(
        ...,
        description='List of schedules. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md',
    )
    kind: Optional[str] = Field(
        None,
        description='Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
    metadata: Optional[metav1.ListMeta] = Field(
        None,
        description='Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds',
    )
