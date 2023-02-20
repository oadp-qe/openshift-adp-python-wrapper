import logging
from enum import Enum

from ocp_resources.resource import NamespacedResource
from src.oadp_constants.resources import ApiGroups

from src.oadp_resources.volsync.replication_destination import ReplicationDestination
from oadp_utils.phase import check_phase

logger = logging.getLogger(__name__)


class VolumeSnapshotRestore(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

    class VolumeSnapshotRestorePhase(Enum):
        SNAPSHOT_RESTORE_DONE = "SnapshotRestoreDone"

        COMPLETED = "Completed"

        IN_PROGRESS = "InProgress"

        FAILED = "Failed"

        PARTIALLY_FAILED = "PartiallyFailed"

        def completed(self):
            return check_phase(self, self.VolumeSnapshotRestorePhase.COMPLETED.value)

        def snapshot_restore_done(self):
            return check_phase(self, self.VolumeSnapshotRestorePhase.SNAPSHOT_RESTORE_DONE.value)

        def in_progress(self):
            return check_phase(self, self.VolumeSnapshotRestorePhase.IN_PROGRESS.value)

        def failed(self):
            return check_phase(self, self.VolumeSnapshotRestorePhase.FAILED.value)

        def partially_failed(self):
            return check_phase(self, self.VolumeSnapshotRestorePhase.PARTIALLY_FAILED.value)

    def replication_destination_completed(self):
        replication_destination_list = ReplicationDestination.get()
        rep_ds_list = [rd for rd in replication_destination_list if
                       rd.labels.get(ReplicationDestination.Label.VOLUME_SNAPSHOT_RESTORE.value) == self.name]
        if len(rep_ds_list) > 1:
            logger.info(f"There are more than one ReplicationDestination for VSR {self.name}")
            return None
        if len(rep_ds_list) == 0:
            logger.info(f"ReplicationDestination was not created for VSR {self.name} or it was already deleted by the "
                        f"controller")
            return None

        return rep_ds_list[0]

    def done(self):
        """
        Check is VSR process is done
        @return: True if the VSR process is not running; False otherwise
        """
        return self.instance.status and self.instance.status.phase != \
            self.VolumeSnapshotRestorePhase.IN_PROGRESS.value

    @classmethod
    def get_by_restore_name(cls, restore_name):
        """
        Returns a list of VSRs by restore name
        @param restore_name: the restore name to get the VSR/s by
        @return: returns a list of VSR/s by restore name restore_name; empty list otherwise
        """
        return list(cls.get(label_selector=f"velero.io/restore-name={restore_name}"))

    @classmethod
    def get_by_source_pvc(cls, src_pvc_name: str, vsr_list: list = None):
        """
        Returns a list of VSRs by source PVC
        @param src_pvc_name: PVC name which the VSR/s point to
        @param vsr_list: the list of VSR/s to filter based on the PVC name; in case not provided, it will be retrieved
        @return: a list of VSRs by source PVC; empty list otherwise
        """
        if not vsr_list:
            vsr_list = list(cls.get())
        vsr_filtered_list = list(filter(
            lambda x: x.instance.spec.volumeSnapshotMoverBackupRef.sourcePVCData.name == src_pvc_name, vsr_list))

        return vsr_filtered_list

    def get_replication_destination(self):
        replication_destination_list = ReplicationDestination.get()
        rep_ds_list = [rd for rd in replication_destination_list if
                       rd.labels.get("datamover.oadp.openshift.io/vsr") == self.name]
        if len(rep_ds_list) > 1:
            logger.error(f"There are more than one ReplicationDestination for VSR {self.name}")
            return None
        if len(rep_ds_list) == 0:
            logger.error(f"ReplicationDestination was not created for VSR {self.name}")
            return None

        return rep_ds_list[0]
