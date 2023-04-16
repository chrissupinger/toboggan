# Standard
from typing import List, Optional, Text, Tuple, Union

# Local
from .commoncontext import DecoCommonContext
from ..utils import ContextAliases

__all__ = ('YieldsContext',)


class YieldsContext(DecoCommonContext):
    
    def __init__(self, type_: Optional[Text] = None, values: Optional[Union[List, Tuple]] = None):
        super().__init__(alias=ContextAliases.yields.name, values=values)
        self.type_ = type_
    
    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, results_in={self.type_}, keys={self.values})'
