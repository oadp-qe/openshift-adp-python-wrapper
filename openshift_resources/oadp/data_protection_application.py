import logging
import wrapper_constants.resources as r

from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class DataProtectionApplication(NamespacedResource):
    api_group = r.ApiGroups.OADP_API_GROUP

    def wait_for_successful_reconciliation(self):
        self.wait_for_condition(condition=r.Condition.CONDITION_RECONCILED, status=r.Status.STATUS_SUC_RECONCILED)

    def wait_for_failed_reconciliation(self):
        self.wait_for_condition(condition=r.Condition.CONDITION_RECONCILED, status=r.Status.STATUS_FAILED_TO_RECONCILE)

