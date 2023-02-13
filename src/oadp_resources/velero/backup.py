from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource
from oadp_utils.wait import wait_for
from oadp_utils.phase import check_phase

from oadp_resources.oadp.datamover.volume_snapshot_backup import VolumeSnapshotBackup


class Backup(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    # BackupPhase is a str representation of the lifecycle phase
    # of a Velero backup.
    class BackupPhase(Enum):

        # New means the backup has been created but not
        # yet processed by the BackupController.
        NEW = "New"

        # FailedValidation means the backup has failed
        # the controller's validations and therefore will not run.
        FAILED_VALIDATION = "FailedValidation"

        # InProgress means the backup is currently executing.
        IN_PROGRESS = "InProgress"

        # Uploading means the backups of Kubernetes resources
        # and creation of snapshots was successful and snapshot data
        # is currently uploading.  The backup is not usable yet.
        UPLOADING = "Uploading"

        # UploadingPartialFailure means the backup of Kubernetes
        # resources and creation of snapshots partially failed (final phase
        # will be PartiallyFailed) and snapshot data is currently uploading.
        # The backup is not usable yet.
        UPLOADING_PARTIAL_FAILURE = "UploadingPartialFailure"

        # Completed means the backup has run successfully without
        # errors.
        COMPLETED = "Completed"

        # PartiallyFailed means the backup has run to completion
        # but encountered 1+ errors backing up individual items.
        PARTIALLY_FAILED = "PartiallyFailed"

        # Failed means the backup ran but encountered an error that
        # prevented it from completing successfully.
        FAILED = "Failed"

        # Deleting means the backup and all its associated data are being deleted.
        DELETING = "Deleting"

    class HookErrorMode(Enum):
        CONTINUE = "Continue"

        # Fail means that an error from a hook is problematic, and the backup should be in
        # error.
        FAIL = "Fail"

    def new(self):
        return check_phase(self, self.BackupPhase.NEW.value)

    def failed_validation(self):
        return check_phase(self, self.BackupPhase.FAILED_VALIDATION.value)

    def in_progress(self):
        return check_phase(self, self.BackupPhase.IN_PROGRESS.value)

    def uploading(self):
        return check_phase(self, self.BackupPhase.UPLOADING.value)

    def uploading_partial_failure(self):
        return check_phase(self, self.BackupPhase.UPLOADING_PARTIAL_FAILURE.value)

    def completed(self):
        return check_phase(self, self.BackupPhase.COMPLETED.value)

    def partially_failed(self):
        return check_phase(self, self.BackupPhase.PARTIALLY_FAILED.value)

    def failed(self):
        return check_phase(self, self.BackupPhase.FAILED.value)

    def deleting(self):
        return check_phase(self, self.BackupPhase.DELETING.value)

    def done(self):
        return not ( self.in_progress() or self.new() )

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

    def wait_for_done(self, wait_timeout=200, sleep=1):
        return wait_for(
            condition_function=self.done,
            description=f"{self.kind} backup to done, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )

    def vsb_exists(self):
        vsbl = VolumeSnapshotBackup.get_by_backup_name(backup_name=self.name)
        if len(vsbl) == 0:
            return False
        return True
