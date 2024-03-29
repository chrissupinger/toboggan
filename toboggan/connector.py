# Standard
from typing import Optional, Text, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .client import Client
from .models import DecoCommonContext, ClientContext
from .utils import ClientAliases, exceptions

__all__ = ('Connector',)


class _ClientContext:
    __slots__ = ('_client',)

    def __init__(self, client: Union[ClientContext, Session, ClientSession]):
        self._client = client
        # Checks for a valid client type.  If not, raises utils.exceptions.UnrecognizedClientType.
        # Default client is Client.block().  This can be changed in user models or during model instantiation.
        if not isinstance(self._client, (ClientContext, Session, ClientSession,)):
            raise exceptions.UnrecognizedClientType(self._client)


class _BaseContext(_ClientContext):
    __slots__ = ('_base_url', '_base_headers', '_session',)

    def __init__(self, base_url, client):
        super().__init__(client=client)
        self._base_url = base_url
        self._base_headers: Optional[DecoCommonContext] = None
        # Checks for the presence of the base_url parameter.  If not, raises utils.exceptions.NoBaseUrl.
        if not base_url:
            raise exceptions.NoBaseUrl()
        self._set_base_headers()
        self._session = self._set_session()

    def _set_base_headers(self) -> None:
        """Mounts base headers to a session based on decorating a constructor with decos.Headers.
        """
        # Set global, base headers for the sessions if using toboggan native clients.
        if isinstance(self._client, ClientContext):
            if self.base_headers:
                self._client.add_base_headers(fields=self.base_headers.values)
        # If user provided requests.Session or aiohttp.ClientSession, set headers directly to the client session.
        elif isinstance(self._client, (Session, ClientSession,)):
            if self.base_headers:
                for key, val in self.base_headers.values.items():
                    self._client.headers[key] = val

    def _set_session(self) -> Union[Session, ClientSession]:
        """Mounts a configured session to constructor.
        """
        # Set session if using one of toboggan's native clients.
        if isinstance(self._client, ClientContext):
            if isinstance(self._client.session, Session):
                return self._client.session
            elif self._client.session == ClientSession:
                return self._client.session(**self._client.settings)
        # Set session if using requests.Session and aiohttp.ClientSession.
        elif isinstance(self._client, (Session, ClientSession,)):
            return self._client

    @property
    def session(self) -> Union[Session, ClientSession]:
        return self._session

    @property
    def base_url(self) -> Text:
        return self._base_url

    @base_url.setter
    def base_url(self, url: Text) -> None:
        self._base_url = url

    @property
    def base_headers(self) -> DecoCommonContext:
        """Returns model if fields were passed using decos.Headers.
        """
        return self._base_headers

    @base_headers.setter
    def base_headers(self, callable_) -> None:
        """Stores headers if a model is decorated w/ decos.Headers.
        """
        self._base_headers = callable_

    @property
    def alias(self) -> Text:
        if isinstance(self.session, Session):
            return ClientAliases.blocking.name
        elif isinstance(self.session, ClientSession):
            return ClientAliases.nonblocking.name


class Connector(_BaseContext):
    """Consolidating constructor for instantiating a session.
    """

    def __init__(
            self,
            base_url: Optional[Text] = None,
            client: Union[ClientContext, Session, ClientSession] = Client.block()):
        super().__init__(base_url=base_url, client=client)
