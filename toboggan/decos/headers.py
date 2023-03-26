# Standard
from functools import wraps
from inspect import isclass, isfunction
from typing import Dict

# Local
from ..models import DecoCommonContext as _HeadersContext
from ..utils import ContextAliases

__all__ = ('Headers',)


class _Context(_HeadersContext):

    def __init__(self, headers: Dict):
        super().__init__()
        self.alias = ContextAliases.headers.name
        self.values = headers

    def __call__(self, callable_):
        @wraps(callable_)
        def arg_handler(*args, **kwargs):
            if isclass(callable_):
                callable_.base_headers = self
                return callable_(*args, **kwargs)
            elif isfunction(callable_):
                args = args + (self,)
                return callable_(*args, **kwargs)
        return arg_handler


class Headers(_Context):

    def __init__(self, headers: Dict) -> None:
        super().__init__(headers=headers)
