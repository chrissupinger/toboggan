# Standard
from __future__ import annotations
from typing import Any, Optional, Union

# Local
from .aliases import AliasSessionType
from .clients import (
    AsyncClient, Client, ClientSession, Session, resolve_client_type,
)

__all__ = ('Connector',)


class MetaclassConnector(type):

    def __new__(cls, name, bases, attrs):
        _cls = super().__new__(cls, name, bases, attrs)
        _cls.base_headers = {}
        _cls.base_query_params = {}
        return _cls


class Connector(metaclass=MetaclassConnector):
    """Base connector class for API clients.
    """

    def __init__(
            self,
            base_url: Optional[str] = None,
            client: Union[Session, Client, ClientSession, AsyncClient] = Session()
        ):
        self.base_url = base_url
        self.client = client
        self.client_type

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'base_url={self.base_url}, '
            f'client={self.client}, '
            f'base_headers={getattr(self, "base_headers", None)}, '
            f'base_query_params={getattr(self, "base_query_params", None)}'
            ')'
        )

    def __call__(
            self,
            base_url: Optional[str] = None,
            client: Optional[Union[Session, Client, ClientSession, AsyncClient]] = None
    ) -> Connector:
        if base_url:
            self.base_url = base_url
        if client:
            self.client = client
        return self

    def session(self) -> Any:
        return self.client

    @property
    def client_type(self) -> AliasSessionType:
        return resolve_client_type(self.client)
