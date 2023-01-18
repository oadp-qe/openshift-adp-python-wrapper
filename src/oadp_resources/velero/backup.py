from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from utils.common import wait_for


class Backup(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    # BackupPhase is a str representation of the lifecycle phase
    # of a Velero backup.
    class BackupPhase(Enum):

        # New means the backup has been created but not
        # yet processed by the BackupController.
        New = "New"

        # FailedValidation means the backup has failed
        # the controller's validations and therefore will not run.
        FailedValidation = "FailedValidation"

        # InProgress means the backup is currently executing.
        InProgress = "InProgress"

        # Uploading means the backups of Kubernetes resources
        # and creation of snapshots was successful and snapshot data
        # is currently uploading.  The backup is not usable yet.
        Uploading = "Uploading"

        # UploadingPartialFailure means the backup of Kubernetes
        # resources and creation of snapshots partially failed (final phase
        # will be PartiallyFailed) and snapshot data is currently uploading.
        # The backup is not usable yet.
        UploadingPartialFailure = "UploadingPartialFailure"

        # Completed means the backup has run successfully without
        # errors.
        Completed = "Completed"

        # PartiallyFailed means the backup has run to completion
        # but encountered 1+ errors backing up individual items.
        PartiallyFailed = "PartiallyFailed"

        # Failed means the backup ran but encountered an error that
        # prevented it from completing successfully.
        Failed = "Failed"

        # Deleting means the backup and all its associated data are being deleted.
        Deleting = "Deleting"

    class HookErrorMode(Enum):
        Continue = "Continue"

        # Fail means that an error from a hook is problematic, and the backup should be in
        # error.
        Fail = "Fail"

    def check_phase(self, phase):
        try:
            manifest = self.instance
        except Exception as e:
            print(f'An error occurred: {e}')
        return manifest.status.phase == phase

    def new(self):
        return self.check_phase(self.BackupPhase.New.value)

    def failed_validation(self):
        return self.check_phase(self.BackupPhase.FailedValidation.value)

    def in_progress(self):
        return self.check_phase(self.BackupPhase.InProgress.value)

    def uploading(self):
        return self.check_phase(self.BackupPhase.Uploading.value)

    def uploading_partial_failure(self):
        return self.check_phase(self.BackupPhase.UploadingPartialFailure.value)

    def completed(self):
        return self.check_phase(self.BackupPhase.Completed.value)

    def partially_failed(self):
        return self.check_phase(self.BackupPhase.PartiallyFailed.value)

    def failed(self):
        return self.check_phase(self.BackupPhase.Failed.value)

    def deleting(self):
        return self.check_phase(self.BackupPhase.Deleting.value)

    def wait_for_success(self):
        return wait_for(
            condition_function=self.completed,
            description=f"wait until backup gets completed, {self.name}",
            sleep=1,
            wait_timeout=240
        )

