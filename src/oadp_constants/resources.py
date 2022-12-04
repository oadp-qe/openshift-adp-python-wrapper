from enum import Enum


class ApiGroups(Enum):
    OADP_API_GROUP = "oadp.openshift.io"
    VELERO_API_GROUP = "velero.io"
    DATAMOVER_OADP_API_GROUP = "datamover.oadp.openshift.io"


class Status(Enum):
    UNAVAILABLE = "Unavailable"
    AVAILABLE = "Available"
    FAILED_TO_RECONCILE = "False"
    SUC_RECONCILED = "True"


class Condition(Enum):
    CONDITION_RECONCILED = "Reconciled"
