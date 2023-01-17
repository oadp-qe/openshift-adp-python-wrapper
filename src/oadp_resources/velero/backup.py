from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from oadp_constants.velero.backup import BackupPhase


class Backup(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    def completed(self):
        try:
            return self.status.phase == BackupPhase.BackupPhaseCompleted.value
        except AttributeError:
            return False
