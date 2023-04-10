# Standard
from functools import wraps
from typing import Dict

# Local
from ..models import DecoCommonContext as _QueryParamsContext
from ..utils import ContextAliases

__all__ = ('Query',)


class _Context(_QueryParamsContext):

    def __init__(self, params: Dict):
        super().__init__(alias=ContextAliases.query.name, values=params)

    def __call__(self, func):
        @wraps(func)
        def arg_handler(*args, **kwargs):
            args = args + (self,)
            return func(*args, **kwargs)
        return arg_handler


class Query(_Context):

    def __init__(self, params: Dict) -> None:
        super().__init__(params=params)
