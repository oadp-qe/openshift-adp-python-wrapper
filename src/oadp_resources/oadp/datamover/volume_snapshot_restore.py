from ocp_resources.resource import NamespacedResource

from oadp_constants.oadp.datamover.volume_snapshot_restore import VolumeSnapshotRestorePhase
from oadp_constants.resources import ApiGroups


class VolumeSnapshotRestore(NamespacedResource):
    api_group = ApiGroups.DATAMOVER_OADP_API_GROUP.value

    def is_done(self):
        """
        Check is VSR process is done
        @return: True if the VSR process is not running; False otherwise
        """
        return self.instance.status and self.instance.status.phase != \
               VolumeSnapshotRestorePhase.SnapMoverRestorePhaseInProgress.value

    @classmethod
    def get_vsrs_by_restore_name(cls, restore_name):
        """
        Returns a list of VSRs by restore name
        @param restore_name: the restore name to get the VSR/s by
        @return: returns a list of VSR/s by restore name restore_name; empty list otherwise
        """
        return list(cls.get(label_selector=f"velero.io/restore-name={restore_name}"))

    @classmethod
    def get_vsrs_by_source_pvc(cls, src_pvc_name: str, vsr_list: list = None):
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

        # TODO: move the following checks to tests repo maybe?
        # if len(vsr_filtered_list) > 1:
        #     raise Exception(f"More than one VSB was found with volumeSnapshotMoverBackupRef "
        #                     f"having source PVC name {src_pvc_name}")
        #
        # if not vsr_list:
        #     raise Exception(f"No VSR was found with volumeSnapshotMoverBackupRef having "
        #                     f"source PVC source {src_pvc_name}")

        return vsr_filtered_list
