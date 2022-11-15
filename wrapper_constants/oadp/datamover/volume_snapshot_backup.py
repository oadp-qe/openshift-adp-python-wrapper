from enum import Enum


class VolumeSnapshotBackupPhase(Enum):
    SnapMoverVolSyncPhaseCompleted = "SnapshotBackupDone"

    SnapMoverBackupPhaseCompleted = "Completed"

    SnapMoverBackupPhaseInProgress = "InProgress"

    SnapMoverBackupPhaseFailed = "Failed"

    SnapMoverBackupPhasePartiallyFailed = "PartiallyFailed"

