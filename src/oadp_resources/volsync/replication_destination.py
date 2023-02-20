import logging
from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource

from oadp_utils.phase import log_status

logger = logging.getLogger(__name__)


class ReplicationDestination(NamespacedResource):
    api_group = ApiGroups.VOLSYC_API_GROUOP.value

    class Label(Enum):
        VOLUME_SNAPSHOT_RESTORE = "datamover.oadp.openshift.io/vsr"

    class ReplicationDestinationCondition(Enum):
        class Type(Enum):
            RECONCILED = "Reconciled"
            SYNCHRONIZING = "Synchronizing"

    def reconciled_synchronizing(self):
        """
        This function check if the ReplicationDestination CR status is reconciled/Synchronizing and returns True,
        otherwise return False.

       Returns:
       boolean: True if ReplicationDestination CR status is reconciled or Synchronizing, False otherwise.
       """
        try:
            log_status(self)
            conditions = self.instance.status.conditions
            conditions_size = len(conditions)
            rd_synchronizing_status = str()
            if conditions_size > 0:
                rd_synchronizing_status = conditions[0].type
            if conditions_size == 2:
                rs_reconcile_status = conditions[1].type
            else:
                rs_reconcile_status = None

            logger.info(f"Current ReplicationDestination condition status is {rd_synchronizing_status}")

            return rd_synchronizing_status == self.ReplicationDestinationCondition.Type.value.SYNCHRONIZING.value and \
                (rs_reconcile_status == self.ReplicationDestinationCondition.Type.value.RECONCILED.value or
                 rs_reconcile_status is None)

        # This will happen only if VSB has completed, and thus RS is removed from the ns
        except AttributeError as e:
            return True
