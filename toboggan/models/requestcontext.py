# Standard
from types import MappingProxyType
from typing import Dict, Optional, Text


__all__ = ('RequestCommonContext',)


class RequestCommonContext:

    def __init__(self, method: Optional[Text], url: Optional[Text]):
        self.method = method
        self.url = url
        self.params: Optional[Dict] = dict()
        self.headers: Optional[Dict] = None
        self.data: Optional[Text] = None
        self.json: Optional[Dict] = None

    @property
    def request_config(self):
        return MappingProxyType(self.__dict__)


class BlockingContext(RequestCommonContext):
    def __init__(self, method, url):
        super().__init__(method, url)


class NonblockingContext(RequestCommonContext):
    def __init__(self, method, url):
        super().__init__(method, url)
