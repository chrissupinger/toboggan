# Standard
from ssl import SSLContext
from typing import Callable, Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import Fingerprint
from typeguard import typechecked

# Local
from .aliases import Request, Response, Send
from .builders import ParametricComplex, ParametricSimple

__all__ = (
    'allow_redirects',
    'connect',
    'delete',
    'get',
    'head',
    'headers',
    'options',
    'params',
    'patch',
    'post',
    'put',
    'returns',
    'sends',
    'ssl',
    'timeout',
    'trace',
)


class _Request:
    __slots__ = ('headers', 'params',)

    def __init__(self):
        self.headers = self._Headers
        self.params = self._Params

    class _Headers(ParametricSimple):
        """Provides access to the headers decorator and can be used to decorate
        classes and instance methods.  A mandatory keyword argument named
        `mapping` is required and is of type `dict`.

        If used to decorate a class, will persist global headers for every
        instance method that consumes a :py:class:`Connector`.

        If used to decorate an instance method, headers will persist for the
        specific HTTP request.

        Usage: ::

            @headers({'Content-Type': 'application/json'})
            class Httpbin(Connector):
                ...

                @headers({'User-Agent': 'MyTestApp/1.0'})
                @get(path='/get')
                def get_(self, **kwargs): pass
        """

        @typechecked
        def __init__(self, mapping: Dict) -> None:
            super().__init__(alias=Request.headers, value=(mapping,))

    class _Params(ParametricSimple):
        """Provides access to the query parameters decorator and can be used to
        decorate classes and instance methods.  A mandatory keyword argument
        named `mapping` is required and is of type `dict`.

        If used to decorate a class, will persist global query parameters for
        every instance method that consumes a :py:class:`Connector`.

        If used to decorate an instance method, query parameters will persist
        for the specific HTTP request.

        Usage: ::

            @params({'sort': 'asc', 'start_date': '2022-01-01'})
            class Httpbin(Connector):
                ...

                @params({'lang': 'en'})
                @get(path='/get')
                def get_(self, **kwargs): pass
        """

        @typechecked
        def __init__(self, mapping: Dict) -> None:
            super().__init__(alias=Request.params, value=(mapping,))


class _RequestOptions:
    __slots__ = ('allow_redirects', 'timeout', 'ssl',)

    def __init__(self):
        self.allow_redirects = self._AllowRedirects
        self.timeout = self._Timeout
        self.ssl = self._Ssl

    class _AllowRedirects(ParametricSimple):

        @typechecked
        def __init__(self, value: bool):
            super().__init__(alias=Request.allow_redirects, value=(value,))

    class _Timeout(ParametricSimple):

        @typechecked
        def __init__(self, value: Union[int, float]):
            super().__init__(alias=Request.timeout, value=(value,))

    class _Ssl(ParametricSimple):

        @typechecked
        def __init__(
                self,
                verify: Union[bool, str, SSLContext, Fingerprint, None] = None,
                cert: Union[tuple, str, None] = None
        ):
            super().__init__(alias=Request.ssl, value=(verify, cert,))


class _Methods:
    __slots__ = (
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

    def __init__(self):
        self.connect = self.Connect
        self.delete = self.Delete
        self.get = self.Get
        self.head = self.Head
        self.options = self.Options
        self.patch = self.Patch
        self.post = self.Post
        self.put = self.Put
        self.trace = self.Trace

    class Connect(ParametricSimple):
        """The CONNECT method establishes a tunnel to the server identified by the
        target resource.

        Usage: ::

            @connect(path='/connect')
            def connect_(self, **kwargs): pass

        References:
            - `CONNECT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/CONNECT>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Delete(ParametricSimple):
        """The DELETE method deletes the specified resource.

        Usage: ::

            @delete(path='/delete')
            def delete_(self, **kwargs): pass

        References:
            - `DELETE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Get(ParametricSimple):
        """The GET method requests a representation of the specified resource. Requests
        using GET should only retrieve data.

        Usage: ::

            @get(path='/get')
            def get_(self, **kwargs): pass

        References:
            - `GET <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET>`_

        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Head(ParametricSimple):
        """The HEAD method asks for a response identical to a GET request, but without
        the response body.

        Usage: ::

            @head(path='/head')
            def head_(self, **kwargs): pass

        References:
            - `HEAD <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Options(ParametricSimple):
        """The OPTIONS method describes the communication options for the target
        resource.

        Usage: ::

            @options(path='/options')
            def options_(self, **kwargs): pass

        References:
            - `OPTIONS <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Patch(ParametricSimple):
        """The PATCH method applies partial modifications to a resource.

        Usage: ::

            @patch(path='/patch')
            def patch_(self, **kwargs): pass

        References:
            - `PATCH <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Post(ParametricSimple):
        """ The POST method submits an entity to the specified resource, often
        causing a change in state or side effects on the server.

        Usage: ::

            @post(path='/post')
            def post_(self, **kwargs): pass

        References:
            - `POST <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Put(ParametricSimple):
        """The PUT method replaces all current representations of the target resource
        with the request payload.

        ::

            @put(path='/put')
            def put_(self, **kwargs): pass

        References:
            - `PUT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )

    class Trace(ParametricSimple):
        """The TRACE method performs a message loop-back test along the path to the
        target resource.

        ::

            @trace(path='/trace')
            def trace_(self, **kwargs): pass

        References:
            - `TRACE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE>`_
        """

        @typechecked
        def __init__(self, path: str) -> None:
            super().__init__(
                alias=Request.method,
                value=(path, self.__class__.__name__.upper(),)
            )


class _Sends:
    __slots__ = ('form_url_encoded', 'json',)

    def __init__(self) -> None:
        self.form_url_encoded = ParametricSimple(
            alias=Request.send_format, value=(Send.data,)
        )
        """Default to sending form-encoded data in the request.

        Usage: ::
        
            @sends.form_url_encoded
            @post(path='/post')
            def post_data(self, body: Body): pass
        """
        self.json = ParametricSimple(
            alias=Request.send_format, value=(Send.json,)
        )
        """Default to sending JSON data in the request.

        Usage: ::
        
            @sends.json
            @post(path='/post')
            def post_json(self, body: Body): pass
        """


class _Returns:
    __slots__ = ('json', 'status_code', 'text',)

    def __init__(self) -> None:
        self.json = self._Json()
        """If wanting to exclusively return the response's JSON object, a flat
        decoration can be used.
        
        Usage: ::
        
            @returns.json
            @get(path='/get')
            def get_(self, **kwargs): pass
            
        Values can be passed to the `key` argument.  This is not required.  If
        used, the values passed will be attempted to be negotiated.  `key` can
        be of type: `list`, `tuple`, `str` or `None`.
        
        Usage: ::
        
            @returns.json(key=...)
            @get(path='/get')
            def get_(self, **kwargs): pass
        """
        self.status_code = ParametricSimple(
            alias=Response.returns, value=(None, Response.status_code,)
        )
        """The response's status code can be exclusively returned.

        Usage: ::
        
            @returns.status_code
            @post(path='/post')
            def post_(self, **kwargs): pass
        """
        self.text = ParametricSimple(
            alias=Response.returns, value=(None, Response.text,)
        )
        """The response's text representation can be exclusively returned.

        Usage: ::
        
            @returns.text
            @delete(path='/delete')
            def delete_(self, **kwargs): pass
        """

    class _Json(ParametricComplex):

        @typechecked
        def __init__(
                self, key: Optional[Union[List, Tuple, str]] = None
        ) -> None:
            super().__init__(
                alias=Response.returns, value=(key, Response.json,)
            )

        def __call__(
                self,
                callable_: Callable = None,
                key: Optional[Union[List, Tuple, str]] = None
        ) -> Callable:
            return super().__call__(callable_=callable_, key=key)


sends = _Sends()
"""Provides access to decorators that allow a method to default to sending
form-encoded data or JSON.  Declaring a subsequent send type will overwrite a
previous declared send type."""
returns = _Returns()
"""Provides access to decorators that allow a method to default to returning
JSON, text or status code when invoked.  Declaring a subsequent return type
will overwrite a previous declared return type."""
_methods = _Methods()
_request = _Request()
_request_options = _RequestOptions()
headers = _request.headers
params = _request.params
allow_redirects = _request_options.allow_redirects
timeout = _request_options.timeout
ssl = _request_options.ssl
connect = _methods.connect
delete = _methods.delete
get = _methods.get
head = _methods.head
options = _methods.options
patch = _methods.patch
post = _methods.post
put = _methods.put
trace = _methods.trace
