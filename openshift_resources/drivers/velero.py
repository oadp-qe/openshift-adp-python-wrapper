from kubernetes_pydantic.drivers.apicore import K8SCustomApiCore

from openshift_resources.drivers.apicore import NewK8SCustomApiCore
from openshift_resources.model.velero.backup import Backup
from wrapper_constants.resources import ApiGroups


class BackupApiCore(NewK8SCustomApiCore):
    model = Backup
    group = ApiGroups.VELERO_API_GROUP.value
    kind = "backups"
    version = "v1"  # just for mock test, should be discovered automatically
