# Standard
from typing import Dict, Optional, Text, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .client import Client
from .models import DecoCommonContext, ClientContext
from .utils import ClientAliases, exceptions

__all__ = ('Connector',)


class _ClientContext:
    __slots__ = ('_client', '_session', '_settings',)

    def __init__(self, client: Union[ClientContext, Session, ClientSession]):
        self._client = client
        # Checks for a valid client type.  If not, raises utils.exceptions.UnrecognizedClientType.
        # Default client is Client.block().  This can be changed in user models or during model instantiation.
        if not isinstance(self._client, (ClientContext, Session, ClientSession,)):
            raise exceptions.UnrecognizedClientType(self._client)
        # Checks for usage of native toboggan client context (Client.block(), Client.nonblock()).
        if isinstance(client, ClientContext):
            self._session, self._settings = client.context
        # If toboggan's client context is not used, checks for requests.Session and aiohttp.ClientSession.
        elif isinstance(client, (Session, ClientSession,)):
            self._session = client

    @property
    def client(self) -> Union[ClientContext, Session, ClientSession]:
        return self._client

    @client.setter
    def client(self, client_) -> None:
        self._client = client_

    @property
    def session(self) -> Union[Session, ClientSession]:
        return self._session

    @property
    def settings(self) -> Dict:
        return self._settings


class _BaseContext(_ClientContext):
    __slots__ = ('_base_url', '_base_headers',)

    def __init__(self, base_url, client):
        super().__init__(client=client)
        self._base_url = base_url
        self._base_headers: Optional[DecoCommonContext] = None
        # Checks for the presence of the base_url parameter.  If not, raises utils.exceptions.NoBaseUrl.
        if not base_url:
            raise exceptions.NoBaseUrl()
        # Set global, base headers for the sessions if requests.Session.  If aiohttp.ClientSession, set headers to
        # settings for consumption at a later time.
        if self.base_headers:
            if isinstance(self._client, ClientContext):
                self._client.add_headers(fields=self.base_headers.values)
            elif isinstance(self._session, Session):
                self._session.headers = self.base_headers.values

    @property
    def base_url(self) -> Text:
        return self._base_url

    @base_url.setter
    def base_url(self, url) -> None:
        self._base_url = url

    @property
    def base_headers(self) -> DecoCommonContext:
        return self._base_headers

    @base_headers.setter
    def base_headers(self, dataclass_) -> None:
        self._base_headers = dataclass_

    @property
    def alias(self) -> Text:
        if isinstance(self.session, Session):
            return ClientAliases.blocking.name
        elif isinstance(self.session, ClientSession) or isinstance(self._client, ClientContext):
            return ClientAliases.nonblocking.name


class Connector(_BaseContext):
    """Consolidating constructor for instantiating a session.
    """

    def __init__(
            self,
            base_url: Optional[Text] = None,
            client: Union[ClientContext, Session, ClientSession] = Client.block()):
        super().__init__(base_url=base_url, client=client)
