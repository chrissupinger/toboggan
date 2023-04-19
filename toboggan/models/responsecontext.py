# Standard
from typing import Dict, Optional, Text, Union

# Third-party
from multidict import CIMultiDictProxy

# Local
from .resultsincontext import ResultsInContext

__all__ = ('ResponseContext',)


class ResponseContext:
    __slots__ = ('status_code', 'headers', 'text', '_json', '_results_in',)

    def __init__(
            self,
            status_code: Optional[int] = None,
            headers: Optional[Union[CIMultiDictProxy, Dict]] = None,
            text: Optional[Text] = None,
            json: Optional[Dict] = None,
            results_in: Optional[ResultsInContext] = None):
        self.status_code = status_code
        self.headers = headers
        self.text = text
        self._json = json
        self._results_in = results_in

    def json(self):
        return self._json
