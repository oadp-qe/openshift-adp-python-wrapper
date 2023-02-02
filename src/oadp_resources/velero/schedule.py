from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups
from oadp_utils.wait import wait_for
from oadp_utils.phase import check_phase


class Schedule(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    class SchedulePhase(Enum):
        NEW = 'New'
        ENABLED = 'Enabled'
        FAILED_VALIDATION = 'FailedValidation'

    def enabled(self):
        return check_phase(self, self.SchedulePhase.ENABLED.value)

    def new(self):
        return check_phase(self, self.SchedulePhase.NEW.value)

    def failed_validation(self):
        return check_phase(self, self.SchedulePhase.FAILED_VALIDATION.value)

    def wait_for_new(self, wait_timeout=200, sleep=5):
        return wait_for(
            self.new,
            description=f"{self.kind} phase to become New, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_enabled(self, wait_timeout=200, sleep=5):
        return wait_for(
            self.enabled,
            description=f"{self.kind} phase to become enabled, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_failed_validation(self, wait_timeout=200, sleep=5):
        return wait_for(
            self.failed_validation,
            description=f"{self.kind} phase to become failed_validation {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )
