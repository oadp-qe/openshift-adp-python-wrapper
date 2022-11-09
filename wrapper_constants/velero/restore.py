from enum import Enum


class RestorePhase(Enum):
    New = 'New'
    FailedValidation = 'FailedValidation'
    InProgress = 'InProgress'
    Completed = 'Completed'
    PartiallyFailed = 'PartiallyFailed'
    Failed = 'Failed'


class HookErrorMode(Enum):
    Continue = 'Continue'
    Fail = 'Fail'


class PolicyType(Enum):
    PolicyTypeNone = 'none'
    PolicyTypeUpdate = 'update'
