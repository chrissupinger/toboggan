# Standard
from typing import Dict

# Local
from ..models import DecoCommonContext as _QueryParamsContext
from ..utils import ContextAliases, StandardCaller as _Caller

__all__ = ('Query',)


class _Context(_QueryParamsContext, _Caller):

    def __init__(self, params: Dict):
        super().__init__(alias=ContextAliases.query.name, values=params)


class Query(_Context):

    def __init__(self, params: Dict) -> None:
        super().__init__(params=params)
