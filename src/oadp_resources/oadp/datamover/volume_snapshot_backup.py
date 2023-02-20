import logging
from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups

from oadp_resources.volsync.replication_source import ReplicationSource
from oadp_utils.phase import check_phase
from oadp_utils.phase import log_status

from oadp_resources.velero.backup import Backup

logger = logging.getLogger(__name__)


class VolumeSnapshotBackup(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

    class VolumeSnapshotBackupPhase(Enum):
        SNAPSHOT_BACKUP_DONE = "SnapshotBackupDone"

        COMPLETED = "Completed"

        IN_PROGRESS = "InProgress"

        FAILED = "Failed"

        PARTIALLY_FAILED = "PartiallyFailed"

    def snapshot_backup_done(self):
        return check_phase(self, self.VolumeSnapshotBackupPhase.SNAPSHOT_BACKUP_DONE.value)

    def completed(self):
        return check_phase(self, self.VolumeSnapshotBackupPhase.COMPLETED.value)

    def in_progress(self):
        return check_phase(self, self.VolumeSnapshotBackupPhase.IN_PROGRESS.value)

    def failed(self):
        return check_phase(self, self.VolumeSnapshotBackupPhase.FAILED.value)

    def partially_failed(self):
        return check_phase(self, self.VolumeSnapshotBackupPhase.PARTIALLY_FAILED.value)

    def done(self):
        """
        Check is VSB process is done
        @return: True if the VSB process is not running; False otherwise
        """
        log_status(self)
        return not self.in_progress()

    @classmethod
    def get_by_backup_name(cls, backup_name):
        """
        Returns a list of VSBs by backup name
        @param backup_name: the backup name to get the VSB/s by
        @return: returns a list of VSB/s by backup name; empty list otherwise
        """
        vsbl = list(cls.get(label_selector=f"{Backup.Label.BACKUP.value}={backup_name}"))

        if len(vsbl) == 0:
            logger.info(f"No VSB was created for backup {backup_name}")

        return vsbl

    @classmethod
    def get_by_source_pvc(cls, src_pvc_name: str, vsb_list: list = None):
        """
        Returns a list of VSBS by source PVC
        @param src_pvc_name: PVC name which the VSB/s point to
        @param vsb_list: the list of VSB/s to filter based on the PVC name; in case not provided, it will be retrieved
        @return: a list of VSBs by source PVC; empty list otherwise
        """
        if not vsb_list:
            vsb_list = list(cls.get())
        vsb_filtered_list = list(filter(
            lambda x: x.instance.status.sourcePVCData.name == src_pvc_name, vsb_list))

        vsbl_size = len(vsb_filtered_list)
        if vsbl_size > 1:
            logger.info(f"More than one VSB was found with source PVC name {src_pvc_name}")

        if vsbl_size == 0:
            logger.info(f"No VSB was found with source PVC name {src_pvc_name}")
            return vsb_filtered_list

        return vsb_filtered_list

    def get_replication_source(self):
        replication_source_list = ReplicationSource.get()
        rep_sr_list = [rs for rs in replication_source_list if
                       rs.labels.get(ReplicationSource.Label.VOLUME_SNAPSHOT_BACKUP.value) == self.name]
        if len(rep_sr_list) > 1:
            logger.info(f"There are more than one ReplicationSource for VSB {self.name}")
            return None
        if len(rep_sr_list) == 0:
            logger.info(f"ReplicationSource was not created for VSB {self.name} or it was already deleted by the "
                        f"controller")
            return None

        return rep_sr_list[0]

    def wait_for_done(self, wait_timeout=240, sleep=5):
        return wait_for(
            condition_function=self.done,
            description=f"{self.kind} to be done, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )
