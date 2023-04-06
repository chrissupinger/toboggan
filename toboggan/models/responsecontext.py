# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional, Text

__all__ = ('ResponseContext',)


@dataclass(slots=True, init=True)
class ResponseContext:
    status_code: Optional[int] = field(default=None)
    text: Optional[Text] = field(default=None)
    _json: Optional[Dict] = field(default=None)
    
    def json(self):
        return self._json
    