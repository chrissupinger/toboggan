# Standard
from typing import Callable, Dict, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

__all__ = ('ClientContext',)


class ClientContext:
    """Model storing context for a client session and its settings.
    """
    __slots__ = ('session', 'settings',)

    def __init__(self, session, settings):
        self.session: Union[Callable, Session, ClientSession] = session
        self.settings: Dict = settings

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, session={self.session}, settings={self.settings})'

    def add_base_headers(self, fields: Dict) -> None:
        """Adds values to an existing session header key constant or add a header key constant and its values to
        client settings.
        """
        if isinstance(self.session, Session):
            for key, val in fields.items():
                self.session.headers[key] = val
        elif self.session == ClientSession:
            self.settings['headers'] = fields
