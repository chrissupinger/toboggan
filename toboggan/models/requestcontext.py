# Standard
from dataclasses import InitVar, asdict, dataclass, field
from typing import Dict, Optional, Text


__all__ = ('RequestCommonContext',)


@dataclass(slots=True, init=True)
class RequestCommonContext:
    method: Optional[Text] = field(default=None)
    url: Optional[Text] = field(default=None)
    params: Optional[Dict] = field(default_factory=dict)
    headers: Optional[Dict] = field(default=None)
    data: Optional[Text] = field(default=None)
    json: Optional[Dict] = field(default=None)

    @property
    def request_config(self):
        return asdict(self)


@dataclass(slots=True, init=True)
class BlockingContext(RequestCommonContext):
    ...


@dataclass(slots=True, init=True)
class NonblockingContext(RequestCommonContext):
    ...
