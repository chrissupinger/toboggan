# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional

# Third-party
from aiohttp import ClientSession
from requests import Session

__all__ = ('SessionContext',)


@dataclass(slots=True, init=True)
class SessionContext:
    """Model storing context for a client session and its settings.
    """
    session: Optional = field(default=None)
    _settings: Dict = field(default_factory=dict)

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, session={self.session}, settings={self.settings})'

    def add_headers(self, fields: Dict) -> None:
        if isinstance(self.session, Session):
            for key, val in fields.items():
                self.session.headers[key] = val
        elif self.session == ClientSession:
            self.settings = dict(headers=fields)

    @property
    def settings(self) -> Dict:
        return self._settings

    @settings.setter
    def settings(self, fields: Dict) -> None:
        for key, val in fields.items():
            self._settings[key] = val
