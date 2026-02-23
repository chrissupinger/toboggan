# Standard
from functools import wraps
from typing import Callable, Dict, Tuple, get_type_hints

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .contexts import (
    _ctx_headers_value,
    _ctx_query_params_value,
    _ctx_returns_type,
    _ctx_returns_json_value,
    _ctx_sends_type,
)
from .wrappers import Wrappers
from toboggan.aliases import AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.connector import Connector
from toboggan.models import TypeKwDump, TypeWrapperMapping

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


class Verb(Wrappers):
    __slots__ = ('__method', '__path',)

    def __init__(self, path: str):
        super().__init__()
        self.__method: str = self.__class__.__name__
        self.__path: str = path

    def __call__(self, func: Callable) -> Callable:
        sig = self._Signature(func)

        @wraps(func)
        def wrapper(*args: Connector, **kwargs):
            kw_dump = sig.kw_dump(**kwargs)
            conn = next(iter(args))
            mapping_wrapper = TypeWrapperMapping(
                conn,
                self.__method,
                self.__path,
                kw_dump,
                _ctx_headers_value.get(),
                _ctx_query_params_value.get(),
                _ctx_sends_type.get(),
                _ctx_returns_type.get(),
                _ctx_returns_json_value.get()
            )
            if conn.client_type is AliasSessionType.AIOHTTP or isinstance(
                    conn.session(), ClientSession
            ):
                return self.wrapper_async(**mapping_wrapper._asdict())
            elif conn.client_type is AliasSessionType.REQUESTS or isinstance(
                    conn.session(), Session
            ):
                return self.wrapper_sync(**mapping_wrapper._asdict())
            raise RuntimeError('...')
        return wrapper

    class _Signature:
        __slots__ = ('__signature',)
        __is_valid: Tuple = (Body, Options, Path, Query, QueryKebab,)

        def __init__(self, func: Callable):
            self.__signature: Dict = get_type_hints(func)

        def __getattr__(self, name: str):
            sig = self.__signature.get(name)
            if sig and sig in self.__is_valid:
                return name
            return None

        def kw_dump(self, **kwargs) -> Dict:
            base = {}
            for sig_key, sig_value in self.__signature.items():
                if sig_value in self.__is_valid:
                    base[sig_key] = TypeKwDump(
                        sig_value, kwargs.get(sig_key)
                    )._asdict()
            return base


connect = type('CONNECT', (Verb,), {})
"""The CONNECT method establishes a tunnel to the server identified by the
target resource

::

    @connect(path='/connect')
    def connect_(self, **kwargs): pass

References:
    - `CONNECT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/CONNECT>`_
"""
delete = type('DELETE', (Verb,), {})
"""The DELETE method deletes the specified resource

::

    @delete(path='/delete')
    def delete_(self, **kwargs): pass

References:
    - `DELETE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE>`_
"""
get = type('GET', (Verb,), {})
"""The GET method requests a representation of the specified resource; requests
using GET should only retrieve data

::

    @get(path='/get')
    def get_(self, **kwargs): pass

References:
    - `GET <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET>`_

"""
head = type('HEAD', (Verb,), {})
"""The HEAD method asks for a response identical to a GET request, but without
the response body

::

    @head(path='/head')
    def head_(self, **kwargs): pass

References:
    - `HEAD <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD>`_
"""
options = type('OPTIONS', (Verb,), {})
"""The OPTIONS method describes the communication options for the target
resource

::

    @options(path='/options')
    def options_(self, **kwargs): pass

References:
    - `OPTIONS <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
"""
patch = type('PATCH', (Verb,), {})
"""The PATCH method applies partial modifications to a resource

::

    @patch(path='/patch')
    def patch_(self, **kwargs): pass

References:
    - `PATCH <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_
"""
post = type('POST', (Verb,), {})
""" The POST method submits an entity to the specified resource, often
causing a change in state or side effects on the server

::

    @post(path='/post')
    def post_(self, **kwargs): pass

References:
    - `POST <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST>`_
"""
put = type('PUT', (Verb,), {})
"""The PUT method replaces all current representations of the target resource
with the request payload

::

    @put(path='/put')
    def put_(self, **kwargs): pass

References:
    - `PUT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT>`_
"""
trace = type('TRACE', (Verb,), {})
"""The TRACE method performs a message loop-back test along the path to the
target resource

::

    @trace(path='/trace')
    def trace_(self, **kwargs): pass

References:
    - `TRACE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE>`_
"""
