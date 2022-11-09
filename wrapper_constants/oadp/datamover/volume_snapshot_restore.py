from enum import Enum


class VolumeSnapshotRestorePhase(Enum):
    SnapMoverRestoreVolSyncPhaseCompleted = "SnapshotRestoreDone"

    SnapMoverRestorePhaseCompleted = "Completed"

    SnapMoverRestorePhaseInProgress = "InProgress"

    SnapMoverRestorePhaseFailed = "Failed"

    SnapMoverRestorePhasePartiallyFailed = "PartiallyFailed"
