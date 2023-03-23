# Standard
from typing import Optional, Text, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .client import Client
from .models import CommonContext, SessionContext
from .utils import ClientAliases, exceptions

__all__ = ('Connector',)


class _ClientContext:
    __slots__ = ('_client',)

    def __init__(self, client: Union[SessionContext, Session, ClientSession]):
        self._client = client

    @property
    def client(self) -> Union[SessionContext, Session, ClientSession]:
        return self._client

    @client.setter
    def client(self, client_type) -> None:
        self._client = client_type


class _BaseContext(_ClientContext):
    __slots__ = ('_base_url', '_base_headers',)

    def __init__(self, base_url, client):
        super().__init__(client=client)
        self._base_url = base_url
        self._base_headers: Optional[CommonContext] = None
        # Checks for the presence of the base_url parameter.  If not, raises utils.exceptions.NoBaseUrl.
        if not base_url:
            raise exceptions.NoBaseUrl()
        # Checks for a valid client type.  If not, raises utils.exceptions.UnrecognizedClientType.
        # Default client is Client.block().  This can be changed in user models or during model instantiation.
        if not isinstance(self.client, (SessionContext, Session, ClientSession)):
            raise exceptions.UnrecognizedClientType(self.client)
        # Set global, base headers for the sessions if requests.Session.  If aiohttp.ClientSession, set headers to
        # settings for consumption at a later time.
        if self.base_headers:
            if isinstance(self.client, SessionContext):
                self.client.add_headers(fields=self.base_headers.values)

    @property
    def base_url(self) -> Text:
        return self._base_url

    @base_url.setter
    def base_url(self, url) -> None:
        self._base_url = url

    @property
    def base_headers(self) -> CommonContext:
        return self._base_headers

    @base_headers.setter
    def base_headers(self, dataclass_) -> None:
        self._base_headers = dataclass_

    @property
    def alias(self) -> Text:
        if isinstance(self.client, SessionContext):
            if isinstance(self.client.session, Session):
                return ClientAliases.blocking.name
            elif self.client.session == ClientSession:
                return ClientAliases.nonblocking.name
        elif isinstance(self.client, Session):
            return ClientAliases.blocking.name
        elif isinstance(self.client, ClientSession):
            return ClientAliases.nonblocking.name


class Connector(_BaseContext):
    """Consolidating constructor for instantiating a session.
    """

    def __init__(
            self,
            base_url: Optional[Text] = None,
            client: Union[SessionContext, Session, ClientSession] = Client.block()):
        super().__init__(base_url=base_url, client=client)
