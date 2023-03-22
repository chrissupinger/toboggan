# Standard
from typing import Optional, Text, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .client import Client
from .models import CommonContext
from .utils import ClientAliases

__all__ = ('Connector',)


class _ClientContext:
    __slots__ = ('_client',)

    def __init__(self, client):
        self._client = client

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client_type):
        self._client = client_type


class _BaseContext(_ClientContext):
    __slots__ = ('_base_url', '_base_headers',)

    def __init__(self, base_url, client):
        super().__init__(client=client)
        self._base_url = base_url
        self._base_headers: Optional[CommonContext] = None

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, url):
        self._base_url = url

    @property
    def base_headers(self):
        return self._base_headers

    @base_headers.setter
    def base_headers(self, dataclass_):
        self._base_headers = dataclass_


class Connector(_BaseContext):
    """Consolidating constructor for instantiating a session.
    """

    def __init__(
            self,
            base_url: Optional[Text] = None,
            client: Union[Client.block, Client.nonblock, ClientSession, Session] = Client.block()):
        super().__init__(base_url=base_url, client=client)
        # Set global, base headers for the sessions if requests.Session.  If aiohttp.ClientSession, set headers to
        # settings to be consumed at a later time.
        if self.base_headers:
            self.client.add_headers(fields=self.base_headers.values)

    @property
    def alias(self) -> Text:
        return ClientAliases.blocking.name if isinstance(self.client.session, Session) else (
            ClientAliases.nonblocking.name if self.client.session == ClientSession else None)
