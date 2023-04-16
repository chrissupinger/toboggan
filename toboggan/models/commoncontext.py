# Standard
from typing import Dict, Iterable, Optional, Text, Union

__all__ = ('DecoCommonContext',)


class DecoCommonContext:
    __slots__ = ('alias', 'values',)

    def __init__(self, alias: Optional[Text], values: Optional[Union[Dict, Iterable]]):
        self.alias = alias
        self.values = values

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, values={self.values})'
