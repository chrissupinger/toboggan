# Standard
from __future__ import annotations
from typing import Dict, Optional, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .aliases import AliasSessionType

__all__ = ('Connector',)


class Connector:
    __slots__ = ('base_url', 'client',)
    base_headers: Dict
    base_query_params: Dict

    def __init__(self, base_url, client = Session()):
        self.base_url: Optional[str] = base_url
        self.client: Optional[Union[Session, ClientSession]] = client

    def __call__(self, base_url = None, client = Session()):
        return self.__init__(base_url=base_url, client=client)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(base_url={self.base_url}, '
            f'client={self.client}, '
            f'base_headers={getattr(self, "base_headers", None)}, '
            f'base_query_params={getattr(self, "base_query_params", None)}'
            ')'
        )

    def session(self):
        return self.client

    @property
    def client_type(self):
        if isinstance(self.session, Session):
            return AliasSessionType.REQUESTS
        elif isinstance(self.session, ClientSession):
            return AliasSessionType.AIOHTTP
        return None
