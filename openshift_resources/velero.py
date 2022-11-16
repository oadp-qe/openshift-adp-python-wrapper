from kubernetes_pydantic.drivers.apiwrapper import K8sWrapApi

from openshift_resources.drivers.velero import BackupApiCore
from openshift_resources.model.velero.backup import Backup


class BackupApi(K8sWrapApi[Backup]):
    model = Backup

    @classmethod
    def new(cls, namespace: str = "openshift", **kwargs) -> "BackupApi":
        kind = cls.model.__name__
        return BackupApi(core=BackupApiCore(namespace=namespace, model=kind, **kwargs))
