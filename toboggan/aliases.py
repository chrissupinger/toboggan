# Standard
from enum import Enum, auto

__all__ = (
    'AdaptersEvalType',
    'AliasReqOptType',
    'AliasReturnType',
    'AliasSessionType',
    'AliasSendsType',
)


class AliasReqOptType(Enum):
    HEADERS = auto()
    QUERY = auto()
    RETRY = auto()


class AliasReturnType(Enum):
    JSON = auto()
    STATUS_CODE = auto()
    TEXT = auto()


class AliasSessionType(Enum):
    AIOHTTP = auto()
    HTTPX_ASYNC = auto()
    HTTPX_SYNC = auto()
    REQUESTS = auto()


class AliasSendsType(Enum):
    DATA = auto()
    JSON = auto()


class AdaptersEvalType(Enum):
    NONE = auto()
    PYDANTIC_V1 = auto()
    PYDANTIC_V2 = auto()
