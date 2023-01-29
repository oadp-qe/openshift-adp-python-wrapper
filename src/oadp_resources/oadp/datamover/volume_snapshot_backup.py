import logging

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups

from oadp_constants.oadp.datamover.volume_snapshot_backup import VolumeSnapshotBackupPhase
from oadp_resources.volsync.replication_source import ReplicationSource

logger = logging.getLogger(__name__)


class VolumeSnapshotBackup(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

    def replication_source_completed(self):
        try:
            conditions = self.status.conditions

        except AttributeError as e:
            return False

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
        return self.instance.status and self.instance.status.phase != \
            VolumeSnapshotBackupPhase.SnapMoverBackupPhaseInProgress.value

    @classmethod
    def get_by_backup_name(cls, backup_name):
        """
        Returns a list of VSBs by backup name
        @param backup_name: the backup name to get the VSB/s by
        @return: returns a list of VSB/s by backup name; empty list otherwise
        """
        return list(cls.get(label_selector=f"velero.io/restore-name={backup_name}"))

    @classmethod
    def get_by_source_pvc(cls, src_pvc_name: str, vsr_list: list = None):
        """
        Returns a list of VSBS by source PVC
        @param src_pvc_name: PVC name which the VSB/s point to
        @param vsr_list: the list of VSB/s to filter based on the PVC name; in case not provided, it will be retrieved
        @return: a list of VSBs by source PVC; empty list otherwise
        """
        if not vsr_list:
            vsr_list = list(cls.get())
        vsr_filtered_list = list(filter(
            lambda x: x.instance.spec.volumeSnapshotMoverBackupRef.sourcePVCData.name == src_pvc_name, vsr_list))

        return vsr_filtered_list

    def get_replication_source(self):
        replication_source_list = ReplicationSource.get()
        rep_ds_list = [rd for rd in replication_source_list if
                       rd.labels.get("datamover.oadp.openshift.io/vsr") == self.name]
        if len(rep_ds_list) > 1:
            logger.error(f"There are more than one ReplicationSource for VSR {self.name}")
            return None
        if len(rep_ds_list) == 0:
            logger.error(f"ReplicationSource was not created for VSR {self.name}")
            return None

        return rep_ds_list[0]
