# Standard
from typing import Dict, Optional, Tuple, Type, Union
from urllib.parse import urlparse

# Third-party
from aiohttp import ClientSession
from requests import Session
from typeguard import typechecked

# Local
from . import exceptions
from .aliases import Client, Scheme
from .client import AiohttpClient, RequestsClient


class Connector:
    __slots__ = ('__base_headers', '__base_params', '__base_url', '__client',)

    @typechecked
    def __init__(
            self,
            base_url: Optional[str] = None,
            client: Union[ClientSession, Session] = RequestsClient()
    ) -> None:
        self.__base_headers: Dict = {}
        self.__base_params: Tuple[Dict, bool] = ({}, False,)
        self.__base_url = base_url
        self.__client = client
        self.__client.headers.update(self.base_headers)
        # if not self.base_url.scheme or \
        #         self.base_url.scheme not in Scheme.__members__:
        #     raise exceptions.InvalidScheme(self.base_url, Scheme.__members__)
        # if not self.base_url.netloc:
        #     raise exceptions.InvalidBaseUrl(self.base_url)

    @property
    def client_alias(self) -> Client:
        if isinstance(self.session, Session):
            return Client.blocking
        if isinstance(self.session, ClientSession):
            return Client.nonblocking

    @property
    def base_headers(self) -> Dict:
        return self.__base_headers

    @property
    def base_params(self) -> Optional[Tuple[Dict, bool]]:
        return self.__base_params

    @property
    def base_url(self) -> urlparse:
        return urlparse(url=self.__base_url)

    @property
    def session(self) -> Union[ClientSession, Session]:
        return self.__client

    @base_headers.setter
    def base_headers(self, mapping: Dict) -> None:
        for key, val in mapping.items():
            self.__base_headers[key.casefold()] = val

    @base_params.setter
    def base_params(self, iterable_: Tuple) -> None:
        self.__base_params = iterable_

    @base_url.setter
    def base_url(self, url: str) -> None:
        self.__base_url = url

    @session.setter
    def session(self, client: Union[ClientSession, Session]) -> None:
        self.__client = client
