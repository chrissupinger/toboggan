# Standard
from functools import wraps
from inspect import isclass
from typing import Callable, Dict, Union

# Local
from .contexts import _ctx_headers_value, _ctx_query_params_value
from toboggan import Connector
from toboggan.aliases import AliasReqOptType

__all__ = ('headers', 'params',)


class Polymorphic:
    __slots__ = ('__context', '__value',)

    def __init__(self, context: AliasReqOptType, value: Dict):
        self.__context = context
        self.__value = value

    def __call__(self, callable_, **kwargs) -> Union[type[Connector], Callable]:
        if isclass(callable_):
            return self._for_class(callable_)
        return self._for_func(callable_)

    def _for_class(self, cls: type[Connector]) -> type[Connector]:
        orig_init = cls.__init__

        @wraps(orig_init)
        def new_init(*args, **kwargs):
            orig_init(*args, **kwargs)

        cls.__init__ = new_init
        if self.__context is AliasReqOptType.HEADERS:
            cls.base_headers.update(self.__value)
        elif self.__context is AliasReqOptType.QUERY:
            cls.base_query_params.update(self.__value)
        return cls

    def _for_func(self, func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args: Connector, **kwargs):
            if self.__context is AliasReqOptType.HEADERS:
                ctx_headers_value = _ctx_headers_value.set(self.__value)
                try:
                    return func(*args, **kwargs)
                finally:
                    _ctx_headers_value.reset(ctx_headers_value)
            elif self.__context is AliasReqOptType.QUERY:
                ctx_query_params_value = _ctx_query_params_value.set(
                    self.__value
                )
                try:
                    return func(*args, **kwargs)
                finally:
                    _ctx_query_params_value.reset(ctx_query_params_value)
            return func(*args, **kwargs)
        return wrapper


class Headers(Polymorphic):

    def __init__(self, value: Dict):
        super().__init__(AliasReqOptType.HEADERS, value)


class Params(Polymorphic):

    def __init__(self, value: Dict):
        super().__init__(AliasReqOptType.QUERY, value)


headers = Headers
params = Params
