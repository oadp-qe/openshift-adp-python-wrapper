import logging
import openshift_resources.constants
from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)

class DataProtectionApplication(NamespacedResource):
    api_group = openshift_resources.constants.OADP_API_GROUP

    def wait_for_successful_reconciliation(self):
        self.wait_for_condition(condition="Reconciled", status="True")

    def wait_for_failed_reconciliation(self):
        self.wait_for_condition(condition="Reconciled", status="False")
