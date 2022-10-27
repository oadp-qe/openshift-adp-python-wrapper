import six
from kubernetes.client import V1LabelSelector
from ocp_resources.resource import NamespacedResource

import wrapper_constants.resources as r
from openshift_resources.base_model import BaseModel
from wrapper_constants.velero.backup import HookErrorMode

"k8s.io/apimachinery/pkg/apis/meta/v1"


class Metadata(BaseModel):
    """
    BackupSpec defines the specification for a Velero backup.
    """

    def __init__(self):
        self._labels = {}  # `json:"labels,omitempty"`


class BackupSpec(BaseModel):
    # BackupSpec defines the specification for a Velero backup.
    """
    BackupSpec defines the specification for a Velero backup.
    """

    def __init__(self):
        # self.Metadata # `json:"metadata,omitempty"`

        self._includedNamespaces: list[str] = []  # `json:"includedNamespaces,omitempty"`

        self._excludedNamespaces: list[str] = []  # `json:"excludedNamespaces,omitempty"`

        self._includedResources: list[str] = []  # `json:"includedResources,omitempty"`

        self._excludedResources: list[str] = []  # `json:"excludedResources,omitempty"`

        self._labelSelector: V1LabelSelector = V1LabelSelector()  # `json:"labelSelector,omitempty"`

        self._orLabelSelectors: list[V1LabelSelector] = []  # `json:"orLabelSelectors,omitempty"`

        self._snapshotVolumes: bool  # `json:"snapshotVolumes,omitempty"`

        self._ttl: str = ""  # `json:"ttl,omitempty"`

        self._includeClusterResources: bool = None  # `json:"includeClusterResources,omitempty"`

        self._hooks: BackupHooks = BackupHooks()  # `json:"hooks,omitempty"`

        self._storageLocation: str = ""  # `json:"storageLocation,omitempty"`

        self._volumeSnapshotLocations: list[str]  # `json:"volumeSnapshotLocations,omitempty"`

        self._defaultVolumesToRestic: bool  # `json:"defaultVolumesToRestic,omitempty"`

        self._orderedResources: {}  # `json:"orderedResources,omitempty"`


class BackupHooks(BaseModel):
    # BackupHooks contains custom behaviors that should be executed at different phases of the backup.
    """
    BackupHooks contains custom behaviors that should be executed at different phases of the backup.
    # Resources are hooks that should be executed when backing up individual instances of a resource.
    """

    def __init__(self):
        self._resources: list[BackupResourceHookSpec] = []  # `json:"resources,omitempty"`


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

    def __init__(self):
        self._name: str = ""  # `json:"name"`

        self._includedNamespaces: list[str] = []  # `json:"includedNamespaces,omitempty"`

        self._excludedNamespaces: list[str] = []  # `json:"excludedNamespaces,omitempty"`

        self._includedResources: list[str] = []  # `json:"includedResources,omitempty"`

        self._excludedResources: list[str] = []  # `json:"excludedResources,omitempty"`

        self._labelSelector: V1LabelSelector = V1LabelSelector()  # `json:"labelSelector,omitempty"`

        self._preHooks: [BackupResourceHook] = []  # `json:"pre,omitempty"`

        self._postHooks: [BackupResourceHook] = []  # `json:"post,omitempty"`


class BackupResourceHook(BaseModel):
    # BackupResourceHook defines a hook for a resource.
    """
    BackupResourceHook defines a hook for a resource.
    exec defines an exec hook.
    """

    def __init__(self):
        self._exec = ExecHook()  # `json:"exec"`


class ExecHook(BaseModel):
    # ExecHook is a hook that uses the pod exec API to execute a command in a container in a pod.
    """
    ExecHook is a hook that uses the pod exec API to execute a command in a container in a pod.

    # _container is the container in the pod where the command should be executed. If not specified,
    # the pod's first container is used.
    # +optional
    """

    def __init__(self):
        self._container = str = ""  # `json:"container,omitempty"`

        self._command: [str] = []  # `json:"command"`

        self._onError: HookErrorMode = None  # `json:"onError,omitempty"`

        self._timeout: str = ""  # `json:"timeout,omitempty"`


class BackupList(BaseModel):
    # +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

    # BackupList is a list of Backups.
    """
    +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
    """

    def __init__(self):
        self._items = [Backup]  # `json:"items"`


class Backup(NamespacedResource):
    api_group = r.ApiGroups.VELERO_API_GROUP.value

    def __init__(self, *args, namespace="openshift-adp", **kwargs):
        super().__init__(*args, namespace=namespace, **kwargs)
        self._spec: BackupSpec = BackupSpec()  # `json:"spec,omitempty"`

    @property
    def spec(self) -> BackupSpec:
        return self._spec

    @classmethod
    def construct_backup(cls, name,
                         **kwargs):
        backup = cls(name=name)
        # initialize self.resource_dict
        backup.to_dict()
        # update additional fields in case they were passed by kwargs
        backup.resource_dict.update(kwargs)
        return backup

    def to_dict(self):
        # to_dict is called in create function, and it overrides self.resource_dict in case
        # one doesn't provide a yaml file. We would like to bypass this problematic behavior
        # by not calling the parent class' implementation in case self.resource_dict is already set
        if self.yaml_file or not self.resource_dict:
            return super().to_dict()
        elif self.resource_dict and not self.resource_dict.get('spec'):
            self.resource_dict['spec'] = self._spec.to_dict()
        return self.resource_dict


if __name__ == "__main__":
    b = Backup.construct_backup("test")
    b.spec.includedNamespaces = ["mysql-persistent"]
    b.to_dict()
    b.create()
