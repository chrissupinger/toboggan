# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional, Text

__all__ = ('ResponseContext',)


@dataclass(slots=True, init=True)
class ResponseContext:
    status_code: Optional[int] = field(default=None)
    _text: Optional[Text] = field(default=None)
    _json: Optional[Dict] = field(default=None)
    
    @property
    def text(self):
        return self._text
    
    def json(self):
        return self._json
    