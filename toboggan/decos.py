# Standard
from typing import Callable, Dict, List, Optional, Tuple, Union

# Third-party
from typeguard import typechecked

# Local
from .aliases import Request, Response, Send, Verb
from .builders import ParametricComplex, ParametricSimple

__all__ = (
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
    'trace',)


class _Headers(ParametricSimple):
    """Template for adding headers to a class or method.
    """

    @typechecked
    def __init__(self, mapping: Dict) -> None:
        super().__init__(alias=Request.headers, value=(mapping,))


class _Method(ParametricSimple):
    """Template for any HTTP method type to add to an instance method.
    """

    @typechecked
    def __init__(self, path: str) -> None:
        super().__init__(
            alias=Request.method,
            value=(path, self.__class__.__name__.upper(),))


class _Params(ParametricSimple):
    """Template for adding query parameters to a class or method.
    """

    @typechecked
    def __init__(self, mapping: Dict) -> None:
        super().__init__(alias=Request.params, value=(mapping,))


class _Sends:
    """Namespace for generating the data format to send.
    """
    __slots__ = ('form_url_encoded', 'json',)

    def __init__(self) -> None:
        self.form_url_encoded = ParametricSimple(
            alias=Request.send_format, value=(Send.data,))
        self.json = ParametricSimple(
            alias=Request.send_format, value=(Send.json,))


class _Returns:
    """Namespace for generating the return type.
    """
    __slots__ = ('json', 'status_code', 'text',)

    def __init__(self) -> None:
        self.json = self._Json()
        self.status_code = ParametricSimple(
            alias=Response.returns, value=(None, Response.status_code,))
        self.text = ParametricSimple(
            alias=Response.returns, value=(None, Response.text,))

    class _Json(ParametricComplex):
        """Template for the JSON return type.  Allows arguments.
        """

        @typechecked
        def __init__(
                self, key: Optional[Union[List, Tuple, str]] = None) -> None:
            super().__init__(
                alias=Response.returns, value=(key, Response.json,))

        def __call__(
                self,
                callable_: Callable = None,
                key: Optional[Union[List, Tuple, str]] = None) -> Callable:
            return super().__call__(callable_=callable_, key=key)


headers = type(Request.headers, (_Headers,), {})
"""Provides access to the headers decorator and can be used to decorate classes
and instance methods.  A mandatory keyword argument named `mapping` is required
and is of type `dict`.

If used to decorate a class, will persist global headers for every instance
method that consumes a :py:class:`Connector`.

If used to decorate an instance method, headers will persist for the specific
HTTP request.

::

    @headers({'Content-Type': 'application/json'})
    class Httpbin(Connector):
        ...
        
        @headers({'User-Agent': 'MyTestApp/1.0'})
        @get(path='/get')
        def get_(self, **kwargs): pass
"""
params = type(Request.params, (_Params,), {})
"""Provides access to the query parameters decorator and can be used to
decorate classes and instance methods.  A mandatory keyword argument named
`mapping` is required and is of type `dict`.

If used to decorate a class, will persist global query parameters for every
instance method that consumes a :py:class:`Connector`.

If used to decorate an instance method, query parameters will persist for the
specific HTTP request.

::

    @params({'sort': 'asc', 'start_date': '2022-01-01'})
    class Httpbin(Connector):
        ...
        
        @params({'lang': 'en'})
        @get(path='/get')
        def get_(self, **kwargs): pass
"""
sends = _Sends()
"""Provides access to decorators that allow a method to default to sending
form-encoded data or JSON.  Declaring a subsequent send type will overwrite a
previous declared send type.

Default to sending form-encoded data in the request.

::

    @sends.form_url_encoded
    @post(path='/post')
    def post_data(self, body: Body): pass
    
Default to sending JSON data in the request.

::

    @sends.json
    @post(path='/post')
    def post_json(self, body: Body): pass
"""
returns = _Returns()
"""Provides access to decorators that allow a method to default to returning
JSON, text or status code when invoked.  Declaring a subsequent return type
will overwrite a previous declared return type.

If wanting to exclusively return the response's JSON object, a flat decoration 
can be used.

::

    @returns.json
    @get(path='/get')
    def get_(self, **kwargs): pass
    
Values can be passed to the `key` argument.  This is not required.  If used, 
the values passed will be attempted to be negotiated.  `key` can  be of type: 
`list`, `tuple`, `str` or `None`.

::

    @returns.json(key=...)
    @get(path='/get')
    def get_(self, **kwargs): pass

The response's status code can be exclusively returned.

::

    @returns.status_code
    @post(path='/post')
    def post_(self, **kwargs): pass

The response's text representation can be exclusively returned.

::

    @returns.text
    @delete(path='/delete')
    def delete_(self, **kwargs): pass
"""
connect = type(Verb.connect, (_Method,), {})
"""The CONNECT method establishes a tunnel to the server identified by the
target resource.

::

    @connect(path='/connect')
    def connect_(self, **kwargs): pass
    
References:
    - `CONNECT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/CONNECT>`_
"""
delete = type(Verb.delete, (_Method,), {})
"""The DELETE method deletes the specified resource.

::

    @delete(path='/delete')
    def delete_(self, **kwargs): pass

References:
    - `DELETE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE>`_
"""
get = type(Verb.get, (_Method,), {})
"""The GET method requests a representation of the specified resource. Requests
using GET should only retrieve data.

::

    @get(path='/get')
    def get_(self, **kwargs): pass
    
References:
    - `GET <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET>`_

"""
head = type(Verb.head, (_Method,), {})
"""The HEAD method asks for a response identical to a GET request, but without
the response body.

::

    @head(path='/head')
    def head_(self, **kwargs): pass
    
References:
    - `HEAD <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD>`_
"""
options = type(Verb.options, (_Method,), {})
"""The OPTIONS method describes the communication options for the target
resource.

::

    @options(path='/options')
    def options_(self, **kwargs): pass

References:
    - `OPTIONS <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
"""
patch = type(Verb.patch, (_Method,), {})
"""The PATCH method applies partial modifications to a resource.

::

    @patch(path='/patch')
    def patch_(self, **kwargs): pass

References:
    - `PATCH <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH>`_
"""
post = type(Verb.post, (_Method,), {})
"""
The POST method submits an entity to the specified resource, often causing a
change in state or side effects on the 
server.
    
::

    @post(path='/post')
    def post_(self, **kwargs): pass

References:
    - `POST <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST>`_
"""
put = type(Verb.put, (_Method,), {})
"""The PUT method replaces all current representations of the target resource
with the request payload.

::

    @put(path='/put')
    def put_(self, **kwargs): pass

References:
    - `PUT <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT>`_
"""
trace = type(Verb.trace, (_Method,), {})
"""The TRACE method performs a message loop-back test along the path to the
target resource.
    
::

    @trace(path='/trace')
    def trace_(self, **kwargs): pass

References:
    - `TRACE <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE>`_
"""
