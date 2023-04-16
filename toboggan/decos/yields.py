# Standard
from typing import List, Optional, Tuple, Union

# Local
from ..models import YieldsContext as _YieldsContext
from ..utils import YieldsAliases, StandardCaller as _Caller

__all__ = ('Yields',)


class _Context(_YieldsContext, _Caller):
    
    def __init__(self, type_, keys):
        super().__init__(type_=type_, values=keys,)


class Yields(_Context):
    
    def __init__(self, type_, values):
        super().__init__(type_, values)
    
    @classmethod
    def json(cls, keys: Optional[Union[List, Tuple]] = None):
        return cls(type_=YieldsAliases.json.name, values=keys)
    
    @classmethod
    def text(cls):
        return cls(type_=YieldsAliases.text.name, values=None)
