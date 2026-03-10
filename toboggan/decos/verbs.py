# Standard
from functools import wraps
from typing import Callable

# Local
from .contexts import (
    _ctx_headers_value,
    _ctx_query_params_value,
    _ctx_retry_value,
    _ctx_returns_type,
    _ctx_returns_json_value,
    _ctx_sends_type,
)
from .evaluators import _EvalSignature
from toboggan.aliases import AliasSessionType
from toboggan.clients import Requests, Settings
from toboggan.connector import Connector

__all__ = (
    'connect',
    'delete',
    'get',
    'head',
    'options',
    'patch',
    'post',
    'put',
    'trace',
)


class Verb:
    __slots__ = ('__method', '__path',)

    def __init__(self, path: str):
        self.__method: str = self.__class__.__name__.capitalize()
        self.__path: str = path

    def __call__(self, func: Callable) -> Callable:
        sig = _EvalSignature(func)

        @wraps(func)
        def wrapper(*args: Connector, **kwargs):
            kw_dump = sig.kw_dump(**kwargs)
            conn = next(iter(args))
            resolve = Settings(
                base_url=conn.base_url,
                path=self.__path,
                base_headers=conn.base_headers,
                base_query_params=conn.base_query_params,
                kw_dump=kw_dump,
                ctx_headers_value=_ctx_headers_value.get(),
                ctx_query_params_value=_ctx_query_params_value.get(),
                ctx_sends_type=_ctx_sends_type.get(),
                ctx_retry_value=_ctx_retry_value.get(),
                ctx_returns_type=_ctx_returns_type.get(),
                ctx_returns_json_key=_ctx_returns_json_value.get(),
            )
            settings = resolve.dump(
                session=conn.session(), method=self.__method
            )
            build_request = Requests(
                client_type=conn.client_type,
                eval_type=sig.eval_type,
                **settings._asdict()
            )
            return build_request.resolve_request()
        return wrapper


class connect(Verb):
    """The CONNECT method establishes a tunnel to the server identified 
    by the target resource.

    ::

        @connect(path='/connect')
        def connect_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class delete(Verb):
    """The DELETE method deletes the specified resource.

    ::

        @delete(path='/delete')
        def delete_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class get(Verb):
    """The GET method requests a representation of the specified 
    resource; requests using GET should only retrieve data.

    ::

        @get(path='/get')
        def get_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class head(Verb):
    """The HEAD method asks for a response identical to a GET request, 
    but without the response body.

    ::

        @head(path='/head')
        def head_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class options(Verb):
    """The OPTIONS method describes the communication options for the 
    target resource.

    ::

        @options(path='/options')
        def options_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class patch(Verb):
    """The PATCH method applies partial modifications to a resource.

    ::

        @patch(path='/patch')
        def patch_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class post(Verb):
    """ The POST method submits an entity to the specified resource, 
    often causing a change in state or side effects on the server.

    ::

        @post(path='/post')
        def post_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class put(Verb):
    """The PUT method replaces all current representations of the target
    resource with the request payload.

    ::

        @put(path='/put')
        def put_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)


class trace(Verb):
    """The TRACE method performs a message loop-back test along the path 
    to the target resource.

    ::

        @trace(path='/trace')
        def trace_(self, **kwargs): pass
    """

    def __init__(self, path: str):
        super().__init__(path=path)
