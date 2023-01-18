from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from oadp_constants.velero.backup import BackupPhase
from oadp_utils.wait import wait_for


class Backup(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    def completed(self):
        try:
            return self.status == BackupPhase.BackupPhaseCompleted.value
        except AttributeError:
            return False

    def wait_for_success(self):
        return wait_for(self.completed, description=f"wait until backup gets completed, {self.name}", sleep=1,
                        wait_timeout=240)
