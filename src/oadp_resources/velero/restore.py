from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups
from oadp_utils.wait import wait_for
from oadp_utils.phase import check_phase


class Restore(NamespacedResource):
    api_group = ApiGroups.VELERO_API_GROUP.value

    # RestorePhase is a str representation of the lifecycle phase
    # of a Velero restore.
    class RestorePhase(Enum):
        # New means the restore has been created but not
        # yet processed by the RestoreController.
        NEW = 'New'

        # FailedValidation means the restore has failed
        # the controller's validations and therefore will not run.
        FAILED_VALIDATION = 'FailedValidation'

        # InProgress means the restore is currently executing.
        IN_PROGRESS = 'InProgress'

        # Completed means the restore has run successfully without
        # errors.
        COMPLETED = 'Completed'

        # PartiallyFailed means the restore has run to completion
        # but encountered 1+ errors restoring up individual items.
        PARTIALLY_FAILED = 'PartiallyFailed'

        # Failed means the restore ran but encountered an error that
        # prevented it from completing successfully.
        FAILED = 'Failed'

    class Label(Enum):
        RESTORE = "velero.io/restore-name"

    class HookErrorMode(Enum):
        CONTINUE = 'Continue'
        FAIL = 'Fail'

    def new(self):
        return check_phase(self, self.RestorePhase.NEW.value)

    def failed_validation(self):
        return check_phase(self, self.RestorePhase.FAILED_VALIDATION.value)

    def in_progress(self):
        return check_phase(self, self.RestorePhase.IN_PROGRESS.value)

    def completed(self):
        return check_phase(self, self.RestorePhase.COMPLETED.value)

    def partially_failed(self):
        return check_phase(self, self.RestorePhase.PARTIALLY_FAILED.value)

    def failed(self):
        return check_phase(self, self.RestorePhase.FAILED.value)

    def wait_for_success(self, wait_timeout=240, sleep=5):
        return wait_for(
            condition_function=self.completed,
            description=f"{self.kind} phase to become completed, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_failure(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.failed,
            description=f"{self.kind} phase to become failed, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_partial_failure(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.partially_failed,
            description=f"{self.kind} phase to become partiallyFailed, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_failed_validation(self, wait_timeout=200, sleep=5):
        return wait_for(
            condition_function=self.failed_validation,
            description=f"{self.kind} phase to become failed_validation, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def wait_for_in_progress(self, wait_timeout=200, sleep=1):
        return wait_for(
            condition_function=self.in_progress,
            description=f"{self.kind} phase to become InProgress, {self.name}",
            wait_timeout=wait_timeout,
            sleep=sleep
        )

    def vsr_exists(self, resource_class):
        vsrl = resource_class.get_by_restore_name(restore_name=self.name)
        if len(vsrl) == 0:
            return False
        return True
