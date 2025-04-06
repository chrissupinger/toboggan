# Standard
from typing import Callable, List, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from . import exceptions

__all__ = ('AiohttpClient', 'RequestsClient',)


class _Client:
    __slots__ = ('session', 'settings',)

    def __init__(
            self, session: Union[Callable, ClientSession, Session]) -> None:
        self.session = session
        self.settings = {}

    def __call__(self, **kwargs):
        attrs = self.__get_session_attrs(self.session)
        for key, val in kwargs.items():
            if key not in attrs:
                raise exceptions.InvalidSessionSetting(
                    setting=key, valid_settings=attrs)
            if isinstance(self.session, Session):
                setattr(self.session, key, val)
            elif self.session is ClientSession:
                self.settings[key] = val
        if self.session is ClientSession:
            return self.session(**self.settings)
        return self.session

    @staticmethod
    def __get_session_attrs(
            session: Union[ClientSession, Session]) -> Union[List, dict.keys]:
        if isinstance(session, Session):
            return session.__attrs__
        if session is ClientSession and isinstance(session, type):
            return session.__init__.__annotations__.keys()


AiohttpClient = _Client(session=ClientSession)
"""Returns an instance of `aiohttp.ClientSession`.

Can accept all `aiohttp.ClientSession` parameters: `base_url`, `connector`, 
`loop`, `cookies`, `headers`, `skip_auto_headers`, `auth`, `json_serialize`, 
`request_class`, `response_class`, `ws_response_class`, `version`, 
`cookie_jar`, `connector_owner`, `raise_for_status`, `read_timeout`, 
`conn_timeout`, `timeout`, `auto_decompress`, `trust_env`, 
`requote_redirect_url`, `trace_configs`, `read_bufsize`, 
`fallback_charset_resolver`, `return`

References:
    - `aiohttp - Client Session <https://docs.aiohttp.org/en/stable/client_reference.html#client-session>`_
"""
RequestsClient = _Client(session=Session())
"""Returns an instance of `requests.Session`.

Can accept all `requests.Session` parameters: `headers`, `cookies`, `auth`, 
`proxies`, `hooks`, `params`, `verify`, `cert`, `adapters`, `stream`, 
`trust_env`, `max_redirects`

References:
    - `Requests - Session Objects <https://requests.readthedocs.io/en/latest/user/advanced/#session-objects>`_
"""
