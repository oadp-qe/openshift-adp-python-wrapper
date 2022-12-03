from enum import Enum


class BackupPhase(Enum):
    # BackupPhase is a str representation of the lifecycle phase
    # of a Velero backup.
    # +kubebuilder:validation:Enum=New;FailedValidation;InProgress;Completed;PartiallyFailed;Failed;Deleting
    """
    BackupPhase is a str representation of the lifecycle phase

# BackupPhaseNew means the backup has been created but not
# yet processed by the BackupController.
    of a Velero backup.
    +kubebuilder:validation:Enum=New;FailedValidation;InProgress;Completed;PartiallyFailed;Failed;Deleting

# BackupPhaseFailedValidation means the backup has failed
# the controller's validations and therefore will not run.
    """

    BackupPhaseNew = "New"

    BackupPhaseFailedValidation = "FailedValidation"

    # BackupPhaseInProgress means the backup is currently executing.
    BackupPhaseInProgress = "InProgress"

    # BackupPhaseUploading means the backups of Kubernetes resources
    # and creation of snapshots was successful and snapshot data
    # is currently uploading.  The backup is not usable yet.
    BackupPhaseUploading = "Uploading"

    # BackupPhaseUploadingPartialFailure means the backup of Kubernetes
    # resources and creation of snapshots partially failed (final phase
    # will be PartiallyFailed) and snapshot data is currently uploading.
    # The backup is not usable yet.
    BackupPhaseUploadingPartialFailure = "UploadingPartialFailure"

    # BackupPhaseCompleted means the backup has run successfully without
    # errors.
    BackupPhaseCompleted = "Completed"

    # BackupPhasePartiallyFailed means the backup has run to completion
    # but encountered 1+ errors backing up individual items.
    BackupPhasePartiallyFailed = "PartiallyFailed"

    # BackupPhaseFailed means the backup ran but encountered an error that
    # prevented it from completing successfully.
    BackupPhaseFailed = "Failed"

    # BackupPhaseDeleting means the backup and all its associated data are being deleted.
    BackupPhaseDeleting = "Deleting"


class HookErrorMode(Enum):
    HookErrorModeContinue = "Continue"

    # HookErrorModeFail means that an error from a hook is problematic, and the backup should be in
    # error.
    HookErrorModeFail = "Fail"