# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional, Text

__all__ = ('DecoCommonContext',)


@dataclass(slots=True, init=True)
class DecoCommonContext:
    alias: Optional[Text] = field(default=None)
    values: Optional[Dict] = field(default=None)

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, values={self.values})'
