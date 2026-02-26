# Standard
from functools import wraps
from typing import Any, Callable, Dict, get_type_hints

# Local
from .contexts import (
    _ctx_headers_value,
    _ctx_query_params_value,
    _ctx_returns_type,
    _ctx_returns_json_value,
    _ctx_sends_type,
)
from toboggan.aliases import AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.clients import ResolverRequest, aiohttp_, requests_
from toboggan.connector import Connector
from toboggan.models import TypeKwDump, TypeKwObjDump

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
        sig = self._Signature(func)

        @wraps(func)
        def wrapper(*args: Connector, **kwargs):
            kw_dump = sig.kw_dump(**kwargs)
            conn = next(iter(args))
            resolve = ResolverRequest(
                base_url=conn.base_url,
                path=self.__path,
                base_headers=conn.base_headers,
                base_query_params=conn.base_query_params,
                kw_dump=kw_dump,
                ctx_headers_value=_ctx_headers_value.get(),
                ctx_query_params_value=_ctx_query_params_value.get(),
                ctx_sends_type=_ctx_sends_type.get(),
                ctx_returns_type=_ctx_returns_type.get(),
                ctx_returns_json_key=_ctx_returns_json_value.get(),
            )
            if conn.client_type is AliasSessionType.AIOHTTP:
                return aiohttp_.request(
                    session=conn.session(),
                    method=self.__method,
                    url=resolve.url(),
                    headers=resolve.headers(),
                    query_params=resolve.query_params(),
                    send=resolve.send(),
                    options=resolve.options(),
                    returns_type=resolve.returns_type,
                    returns_json_key=resolve.returns_json_key
                )
            elif conn.client_type is AliasSessionType.REQUESTS:
                return requests_.request(
                    session=conn.session(),
                    method=self.__method,
                    url=resolve.url(),
                    headers=resolve.headers(),
                    query_params=resolve.query_params(),
                    send=resolve.send(),
                    options=resolve.options(),
                    returns_type=resolve.returns_type,
                    returns_json_key=resolve.returns_json_key
                )
            raise RuntimeError('...')
        return wrapper

    class _Signature:
        __slots__ = ('__signature',)

        def __init__(self, func: Callable):
            self.__signature: Dict[str, Any] = get_type_hints(func)

        def kw_dump(self, **kwargs) -> TypeKwDump:
            base = TypeKwDump()
            for sig_key, sig_value in self.__signature.items():
                if sig_value in (Body, Path, Query, QueryKebab,):
                    base.dump[sig_key] = TypeKwObjDump(
                        sig_value, kwargs.get(sig_key)
                    )
                if sig_value is Options:
                    opts = {
                        key: val for key, val in kwargs.items()
                        if key not in base.dump.keys()
                    }
                    base.dump[sig_key] = TypeKwObjDump(
                        sig_value, opts
                    )
            return base


class connect(Verb):
    """The CONNECT method establishes a tunnel to the server identified by the
    target resource

    ::

        @connect(path='/connect')
        def connect_(self, **kwargs): pass

    References:
        - `CONNECT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/CONNECT>`_
    """

    def __init__(self, path):
        super().__init__(path)


class delete(Verb):
    """The DELETE method deletes the specified resource

    ::

        @delete(path='/delete')
        def delete_(self, **kwargs): pass

    References:
        - `DELETE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE>`_
    """

    def __init__(self, path):
        super().__init__(path)


class get(Verb):
    """The GET method requests a representation of the specified resource;
    requests using GET should only retrieve data

    ::

        @get(path='/get')
        def get_(self, **kwargs): pass

    References:
        - `GET <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET>`_

    """

    def __init__(self, path):
        super().__init__(path)


class head(Verb):
    """The HEAD method asks for a response identical to a GET request, but
    without the response body

    ::

        @head(path='/head')
        def head_(self, **kwargs): pass

    References:
        - `HEAD <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD>`_
    """

    def __init__(self, path):
        super().__init__(path)


class options(Verb):
    """The OPTIONS method describes the communication options for the target
    resource

    ::

        @options(path='/options')
        def options_(self, **kwargs): pass

    References:
        - `OPTIONS <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
    """

    def __init__(self, path):
        super().__init__(path)


class patch(Verb):
    """The PATCH method applies partial modifications to a resource

    ::

        @patch(path='/patch')
        def patch_(self, **kwargs): pass

    References:
        - `PATCH <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_
    """

    def __init__(self, path):
        super().__init__(path)


class post(Verb):
    """ The POST method submits an entity to the specified resource, often
    causing a change in state or side effects on the server

    ::

        @post(path='/post')
        def post_(self, **kwargs): pass

    References:
        - `POST <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST>`_
    """

    def __init__(self, path):
        super().__init__(path)


class put(Verb):
    """The PUT method replaces all current representations of the target
    resource with the request payload

    ::

        @put(path='/put')
        def put_(self, **kwargs): pass

    References:
        - `PUT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT>`_
    """

    def __init__(self, path):
        super().__init__(path)


class trace(Verb):
    """The TRACE method performs a message loop-back test along the path to the
    target resource

    ::

        @trace(path='/trace')
        def trace_(self, **kwargs): pass

    References:
        - `TRACE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE>`_
    """

    def __init__(self, path):
        super().__init__(path)
