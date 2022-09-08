import logging
import wrapper_constants.resources as r

from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = r.ApiGroups.OADP_API_GROUP.value

    def wait_for_successful_reconciliation(self):
        self.wait_for_condition(condition=r.Condition.CONDITION_RECONCILED.value,
                                status=r.Status.SUC_RECONCILED.value)

    def wait_for_failed_reconciliation(self):
        self.wait_for_condition(condition=r.Condition.CONDITION_RECONCILED.value,
                                status=r.Status.FAILED_TO_RECONCILE.value)
