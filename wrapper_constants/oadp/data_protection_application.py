from enum import Enum


class Provider(Enum):
    aws = 'aws'
    gcp = 'gpc'
    azure = 'azure'


class AccessMode(Enum):
    ReadOnly = 'ReadOnly'
    ReadWrite = 'ReadWrite'


class LogLevel(Enum):
    trace = 'trace'
    debug = 'debug'
    info = 'info'
    warning = 'warning'
    error = 'error'
    fatal = 'fatal'
    panic = 'panic'
