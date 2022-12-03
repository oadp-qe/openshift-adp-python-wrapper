from enum import Enum


class BackupStorageLocationAccessMode(Enum):
    BackupStorageLocationAccessModeReadOnly = 'ReadOnly'
    BackupStorageLocationAccessModeReadWrite = 'ReadWrite'


class BackupStorageLocationPhase(Enum):
    Available = 'Available'
    Unavailable = 'Unavailable'

