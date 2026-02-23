# Standard
from typing import Dict, NewType

__all__ = ('Body', 'Options', 'Path', 'Query', 'QueryKebab',)

Body       = NewType(name='Body', tp=Dict)
Options    = NewType(name='Options', tp=Dict)
Path       = NewType(name='Path', tp=str)
Query      = NewType(name='Query', tp=str)
QueryKebab = NewType(name='QueryKebab', tp=str)
