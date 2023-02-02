import logging

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups

from oadp_constants.oadp.datamover.volume_snapshot_backup import VolumeSnapshotBackupPhase
from oadp_resources.volsync.replication_source import ReplicationSource
from oadp_utils.wait import wait_for

logger = logging.getLogger(__name__)


class VolumeSnapshotBackup(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

    def replication_source_completed(self):
        try:
            conditions = self.status.conditions
        
        # This will happen only if VSB has completed, and thus RS is removed from the ns
        except AttributeError as e:
            return True

        return len(conditions) > 1 and \
            conditions[0].type == "Reconciled" and \
            conditions[0].type.status and \
            conditions[1].type == "Synchronizing" and \
            not conditions[1].status

    def done(self):
        """
        Check is VSB process is done
        @return: True if the VSB process is not running; False otherwise
        """
        vsb_status = self.instance.status
        return vsb_status and vsb_status.phase != \
            VolumeSnapshotBackupPhase.SnapMoverBackupPhaseInProgress.value

    @classmethod
    def get_by_backup_name(cls, backup_name):
        """
        Returns a list of VSBs by backup name
        @param backup_name: the backup name to get the VSB/s by
        @return: returns a list of VSB/s by backup name; empty list otherwise
        """
        vsbl = list(cls.get(label_selector=f"velero.io/backup-name={backup_name}"))

        if len(vsbl) == 0:
            logger.error(f"No VSB was created for backup {backup_name}")

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
            logger.error(f"More than one VSB was found with source PVC name {src_pvc_name}")

        if vsbl_size == 0:
            logger.error(f"No VSB was found with source PVC name {src_pvc_name}")

        return vsb_filtered_list[0]

    def get_replication_source(self):
        replication_source_list = ReplicationSource.get()
        rep_sr_list = [rd for rd in replication_source_list if
                       rd.labels.get("datamover.oadp.openshift.io/vsb") == self.name]
        if len(rep_sr_list) > 1:
            logger.error(f"There are more than one ReplicationSource for VSB {self.name}")
            return None
        if len(rep_sr_list) == 0:
            logger.error(f"ReplicationSource was not created for VSB {self.name}")
            return None

        return rep_sr_list[0]

    def wait_for_done(self, wait_timeout=240, sleep=5):
        return wait_for(
            condition_function=self.done,
            description=f"{self.kind} to done, {self.name}",
            sleep=sleep,
            wait_timeout=wait_timeout
        )
