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
        New = 'New'

        # FailedValidation means the restore has failed
        # the controller's validations and therefore will not run.
        FailedValidation = 'FailedValidation'

        # InProgress means the restore is currently executing.
        InProgress = 'InProgress'

        # Completed means the restore has run successfully without
        # errors.
        Completed = 'Completed'

        # PartiallyFailed means the restore has run to completion
        # but encountered 1+ errors restoring up individual items.
        PartiallyFailed = 'PartiallyFailed'

        # Failed means the restore ran but encountered an error that
        # prevented it from completing successfully.
        Failed = 'Failed'

    class HookErrorMode(Enum):
        Continue = 'Continue'
        Fail = 'Fail'

    def new(self):
        return check_phase(self, self.RestorePhase.New.value)

    def failed_validation(self):
        return check_phase(self, self.RestorePhase.FailedValidation.value)

    def in_progress(self):
        return check_phase(self, self.RestorePhase.InProgress.value)

    def completed(self):
        return check_phase(self, self.RestorePhase.Completed.value)

    def partially_failed(self):
        return check_phase(self, self.RestorePhase.PartiallyFailed.value)

    def failed(self):
        return check_phase(self, self.RestorePhase.Failed.value)

    def wait_for_success(self):
        return wait_for(
            condition_function=self.completed,
            description=f"wait until {self.kind} gets completed, {self.name}",
        )

    def wait_for_failure(self):
        return wait_for(
            condition_function=self.failed,
            description=f"wait until {self.kind} gets failed, {self.name}",
        )

    def wait_for_partial_failure(self):
        return wait_for(
            condition_function=self.partially_failed,
            description=f"wait until {self.kind} gets partiallyFailed, {self.name}",
        )

    def wait_for_failed_validation(self):
        return wait_for(
            condition_function=self.failed_validation,
            description=f"wait until {self.kind} gets failed due validation error, {self.name}",
        )

    def wait_for_in_progress(self):
        return wait_for(
            condition_function=self.in_progress,
            description=f"wait until {self.kind} phase is InProgress, {self.name}",
        )
