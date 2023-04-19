# Standard
from typing import List, Optional, Tuple, Union

# Local
from ..models import ResultsInContext as _ResultsInContext
from ..utils import ResultsInAliases, StandardCaller as _Caller

__all__ = ('ResultsIn',)


class _Context(_ResultsInContext, _Caller):
    
    def __init__(self, type_, keys):
        super().__init__(type_=type_, values=keys,)


class ResultsIn(_Context):
    
    def __init__(self, type_, values):
        super().__init__(type_, values)
    
    @classmethod
    def status_code(cls):
        return cls(type_=ResultsInAliases.status_code.name, values=None)
    
    @classmethod
    def text(cls):
        return cls(type_=ResultsInAliases.text.name, values=None)

    @classmethod
    def json(cls, keys: Optional[Union[List, Tuple]] = None):
        return cls(type_=ResultsInAliases.json.name, values=keys)
