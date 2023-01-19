from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups
from oadp_utils.wait import wait_for
from oadp_utils.phase import check_phase


class Schedule(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    class SchedulePhase(Enum):
        New = 'New'
        Enabled = 'Enabled'
        FailedValidation = 'FailedValidation'

    def enabled(self):
        return check_phase(self, self.SchedulePhase.Enabled.value)

    def new(self):
        return check_phase(self, self.SchedulePhase.New.value)

    def failed_validation(self):
        return check_phase(self, self.SchedulePhase.FailedValidation.value)

    def wait_for_new(self):
        return wait_for(self.new, description=f"wait until schedule phase is New, {self.name}")

    def wait_for_enabled(self):
        return wait_for(self.enabled, description=f"wait until schedule phase gets enabled, {self.name}")

    def wait_for_failed_validation(self):
        return wait_for(self.failed_validation, description=f"wait until schedule gets failed due to validation error "
                                                            f"{self.name}")
