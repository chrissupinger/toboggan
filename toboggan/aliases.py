# Standard
from enum import Enum, auto

__all__ = (
    'AliasReqOptType', 'AliasReturnType', 'AliasSessionType', 'AliasSendsType',
)


class AliasReqOptType(Enum):
    HEADERS = auto()
    QUERY = auto()


class AliasReturnType(Enum):
    JSON = auto()
    STATUS_CODE = auto()
    TEXT = auto()


class AliasSessionType(Enum):
    AIOHTTP = auto()
    HTTPX = auto()
    NONE = auto()
    REQUESTS = auto()


class AliasSendsType(Enum):
    DATA = auto()
    JSON = auto()
