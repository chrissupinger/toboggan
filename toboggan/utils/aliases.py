# Standard
from enum import Enum, auto

__all__ = ('ClientAliases', 'ContextAliases', 'ResultsInAliases',)


class ClientAliases(Enum):
    blocking = auto()
    nonblocking = auto()


class ContextAliases(Enum):
    headers = auto()
    method = auto()
    query = auto()
    results_in = auto()


class ResultsInAliases(Enum):
    json = auto()
    status_code = auto()
    text = auto()
