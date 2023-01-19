from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from oadp_utils.wait import wait_for
from oadp_utils.phase import check_phase


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

    def new(self):
        return check_phase(self, self.BackupPhase.New.value)

    def failed_validation(self):
        return check_phase(self, self.BackupPhase.FailedValidation.value)

    def in_progress(self):
        return check_phase(self, self.BackupPhase.InProgress.value)

    def uploading(self):
        return check_phase(self, self.BackupPhase.Uploading.value)

    def uploading_partial_failure(self):
        return check_phase(self, self.BackupPhase.UploadingPartialFailure.value)

    def completed(self):
        return check_phase(self, self.BackupPhase.Completed.value)

    def partially_failed(self):
        return check_phase(self, self.BackupPhase.PartiallyFailed.value)

    def failed(self):
        return check_phase(self, self.BackupPhase.Failed.value)

    def deleting(self):
        return check_phase(self, self.BackupPhase.Deleting.value)

    def wait_for_success(self, wait_timeout=240, sleep=5):
        return wait_for(
            condition_function=self.completed,
            description=f"{self.kind} phase to become completed, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def wait_for_failure(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.failed,
            description=f"{self.kind} phase to become failed, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def wait_for_partial_failure(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.partially_failed,
            description=f"{self.kind} phase to become partiallyFailed, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def wait_for_failed_validation(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.failed_validation,
            description=f"{self.kind} phase to become failed_validation, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def wait_for_in_progress(self, wait_timeout=200, sleep=1):
        return wait_for(
            condition_function=self.in_progress,
            description=f"{self.kind} phase to become InProgress, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def wait_for_deleting(self, wait_timeout=200, sleep=1):
        return wait_for(
            condition_function=self.deleting,
            description=f"{self.kind} phase to become deleting, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )
