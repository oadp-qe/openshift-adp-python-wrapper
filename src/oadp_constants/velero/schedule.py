from enum import Enum


class SchedulePhase(Enum):
    SchedulePhaseNew = 'New'
    SchedulePhaseEnabled = 'Enabled'
    SchedulePhaseFailedValidation = 'FailedValidation'
