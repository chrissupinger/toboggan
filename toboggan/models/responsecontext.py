# Standard
from typing import Dict, Optional, Text, Union

# Third-party
from multidict import CIMultiDictProxy

__all__ = ('ResponseContext',)


class ResponseContext:
    __slots__ = ('status_code', 'headers', 'text', '_json',)

    def __init__(
            self,
            status_code: Optional[int],
            headers: Optional[Union[CIMultiDictProxy, Dict]],
            text: Optional[Text],
            json: Optional[Dict] = None):
        self.status_code = status_code
        self.headers = headers
        self.text = text
        self._json = json
    
    def json(self):
        return self._json
    