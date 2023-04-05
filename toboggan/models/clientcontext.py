# Standard
from typing import Dict

# Third-party
from aiohttp import ClientSession
from requests import Session

__all__ = ('ClientContext',)


class ClientContext:
    """Model storing context for a client session and its settings.
    """
    __slots__ = ('session', '_settings',)

    def __init__(self, session, settings):
        self.session = session
        self._settings = settings

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, session={self.session}, settings={self.settings})'

    def add_headers(self, fields: Dict) -> None:
        if isinstance(self.session, Session):
            for key, val in fields.items():
                self.session.headers[key] = val
        elif self.session == ClientSession:
            self.settings['headers'] = fields

    @property
    def settings(self) -> Dict:
        return self._settings

    @settings.setter
    def settings(self, fields: Dict) -> None:
        for key, val in fields.items():
            self._settings[key] = val
