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
    """Provides access to the headers decorator and can be used to 
    decorate classes and instance methods.  Argument is of type `dict`.

    If used to decorate a class, will persist global headers for every 
    instance method that consumes a :py:class:`Connector`.

    If used to decorate an instance method, headers will persist for the 
    specific HTTP request.

    ::

        @headers({'Content-Type': 'application/json'})
        class Httpbin(Connector):
            
            @headers({'User-Agent': 'MyTestApp/1.0'})
            @get(path='/get')
            def get_request(self): pass
    """

    def __init__(self, value: Dict):
        super().__init__(AliasReqOptType.HEADERS, value)


class Params(Polymorphic):
    """Provides access to the query parameters decorator and can be used 
    to decorate classes and instance methods.  IArgument is of type 
    `dict`.

    If used to decorate a class, will persist global query parameters 
    for every instance method that consumes a :py:class:`Connector`.

    If used to decorate an instance method, query parameters will 
    persist for the specific HTTP request.

    ::

        @params({'sort': 'asc', 'start_date': '2022-01-01'})
        class Httpbin(Connector):
            
            @params({'lang': 'en'})
            @get(path='/get')
            def get_request(self): pass
    """

    def __init__(self, value: Dict):
        super().__init__(AliasReqOptType.QUERY, value)


headers = Headers
params = Params
