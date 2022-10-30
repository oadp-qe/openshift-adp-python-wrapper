from typing import List, Dict, Optional, Any

from kubernetes.dynamic import DynamicClient
from pydantic import BaseModel, Field
from resources.io.k8s.apimachinery.pkg.apis.meta.v1 import LabelSelector, ObjectMeta

from wrapper_constants.velero.backup import HookErrorMode, BackupPhase

class Metadata(BaseModel):
    """
    BackupSpec defines the specification for a Velero backup.json.
    """

    labels: Optional[dict]  # `json:"labels,omitempty"`


class ExecHook(BaseModel):
    # ExecHook is a hook that uses the pod exec API to execute a command in a container in a pod.
    """
    ExecHook is a hook that uses the pod exec API to execute a command in a container in a pod.

    # _container is the container in the pod where the command should be executed. If not specified,
    # the pod's first container is used.
    # +optional
    """

    container: Optional[str]
    command: Optional[List[str]]
    onError: Optional[HookErrorMode]
    timeout: Optional[str]


class BackupResourceHook(BaseModel):
    # BackupResourceHook defines a hook for a resource.
    """
    BackupResourceHook defines a hook for a resource.
    exec defines an exec hook.
    """

    exec: Optional[ExecHook]


class BackupResourceHookSpec(BaseModel):
    # BackupResourceHookSpec defines one or more BackupResourceHooks that should be executed based on
    # the rules defined for namespaces, resources, and label selector.
    """
    BackupResourceHookSpec defines one or more BackupResourceHooks that should be executed based on

    # Name is the name of this hook.
    # IncludedNamespaces specifies the namespaces to which this hook spec applies. If empty, it applies
    # to all namespaces.
    the rules defined for namespaces, resources, and label selector.
    """

    name: Optional[str]
    includedNamespaces: Optional[List[str]]
    excludedNamespaces: Optional[List[str]]
    includedResources: Optional[List[str]]
    excludedResources: Optional[List[str]]
    labelSelector: LabelSelector
    preHooks: Optional[List[BackupResourceHook]]
    postHooks: Optional[List[BackupResourceHook]]



class BackupHooks(BaseModel):
    # BackupHooks contains custom behaviors that should be executed at different phases of the backup.json.
    """
    BackupHooks contains custom behaviors that should be executed at different phases of the backup.json.
    # Resources are hooks that should be executed when backing up individual instances of a resource.
    """
    resources: Optional[List[BackupResourceHookSpec]]


class BackupSpec(BaseModel):
    # BackupSpec defines the specification for a Velero backup.json.
    """
    BackupSpec defines the specification for a Velero backup.json.
    """

    # self.Metadata # `json:"metadata,omitempty"`

    includedNamespaces: Optional[List[str]]
    excludedNamespaces: Optional[List[str]]
    includedResources: Optional[List[str]]
    excludedResources: Optional[List[str]]
    labelSelector: Optional[LabelSelector]
    orLabelSelectors: Optional[List[LabelSelector]]
    snapshotVolumes: Optional[bool]  # `json:"snapshotVolumes,omitempty"`
    ttl: Optional[str]
    includeClusterResources: Optional[bool]
    hooks: Optional[BackupHooks]
    storageLocation: Optional[str]
    volumeSnapshotLocations: Optional[List[str]]  # `json:"volumeSnapshotLocations,omitempty"`
    defaultVolumesToRestic: Optional[bool]  # `json:"defaultVolumesToRestic,omitempty"`
    orderedResources: Optional[Dict]  # `json:"orderedResources,omitempty"`


class BackupStatus(BaseModel):
    completionTimestamp: Optional[Any]
    csiVolumeSnapshotsAttempted: Optional[int]
    csiVolumeSnapshotsCompleted: Optional[int]
    errors: Optional[int]
    expiration: Optional[Any]
    failureReason: Optional[str]
    formatVersion: Optional[str]
    phase: Optional[BackupPhase]
    progress: Optional[Any]
    startTimestamp: Optional[Any]
    validationErrors: Optional[Any]
    version: Optional[int]
    volumeSnapshotsAttempted: Optional[int]
    volumeSnapshotsCompleted: Optional[int]
    warnings: Optional[int]


class Backup(BaseModel):
    apiVersion: Optional[str]
    kind :str = Field(__qualname__)
    metadata: Optional[ObjectMeta]
    spec: Optional[BackupSpec]
    status: Optional[BackupStatus]


class BackupBuilder:

    # TODO: define better
    def __init__(self, *args, **kwargs):
        self.resource = Backup,
        # TODO: add client
        self.client: DynamicClient # type DynamicClient

