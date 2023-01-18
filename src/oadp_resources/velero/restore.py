from enum import Enum

from ocp_resources.resource import NamespacedResource
from oadp_constants.resources import ApiGroups


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

    def check_phase(self, phase):
        try:
            manifest = self.instance
        except Exception as e:
            print(f'An error occurred: {e}')
        return manifest.status.phase == phase

    def new(self):
        return self.check_phase(self.RestorePhase.New.value)

    def failed_validation(self):
        return self.check_phase(self.RestorePhase.FailedValidation.value)

    def in_progress(self):
        return self.check_phase(self.RestorePhase.InProgress.value)

    def completed(self):
        return self.check_phase(self.RestorePhase.Completed.value)

    def partially_failed(self):
        return self.check_phase(self.RestorePhase.PartiallyFailed.value)

    def failed(self):
        return self.check_phase(self.RestorePhase.Failed.value)
