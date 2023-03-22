# Standard
from enum import Enum, auto

__all__ = ('ClientAliases', 'ContextAliases',)


class ClientAliases(Enum):
    blocking = auto()
    nonblocking = auto()


class ContextAliases(Enum):
    headers = auto()
    method = auto()
    query = auto()
    returns = auto()
