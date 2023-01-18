from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups
from oadp_constants.velero.restore import RestorePhase


class Restore(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    def completed(self):
        try:
            return self.status.phase == RestorePhase.BackupPhaseCompleted.value
        except AttributeError:
            return False
