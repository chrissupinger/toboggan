# Standard
from typing import Callable, Dict, List, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from . import exceptions
from .aliases import Request

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
    def __get_session_attrs(session: Union[ClientSession, Session]) -> List:
        if isinstance(session, Session):
            return session.__attrs__
        if session is ClientSession and isinstance(session, type):
            return session.__init__.__annotations__.keys()


AiohttpClient = _Client(session=ClientSession)
RequestsClient = _Client(session=Session())
