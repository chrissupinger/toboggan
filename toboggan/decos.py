# Standard
from functools import wraps
from inspect import isclass, isfunction, signature
from typing import Callable, Coroutine, Dict, List, Optional, Tuple, Union

# Third-party
from typeguard import typechecked

# Local
from . import exceptions
from .aliases import Client, Request, Response, Verb
from .builders import Message
from .connector import Connector
from .models import Configure, ResponseObject

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
    'trace',)


class _CommonContext:
    """The common context shared across every class-level and method-level
    decorator.
    """
    __slots__ = ('alias', 'value',)

    @typechecked
    def __init__(
            self,
            alias: Union[Request, Response],
            value: Optional[Union[Dict, List, Tuple, str]]) -> None:
        self.alias = alias
        self.value = value

    def __repr__(self) -> str:
        return \
            f'{self.__class__.__name__}' \
            f'{tuple(f"{ele}={getattr(self, ele)}" for ele in self.__slots__)}'

    def __call__(
            self,
            callable_: Union[Connector, Callable]
    ) -> Union[Connector, Callable, ResponseObject]:
        if isclass(callable_):
            return self.__for_class(callable_)
        if isfunction(callable_):
            return self.__for_func(callable_)

    def __for_class(self, cls):
        """Wraps a class when it's decorated.  Enables chaining of more than
        one class decorator.  Enables the setting of :py:class:`Connector`
        attributes that will be consumed by :py:class:`Configure.Request`.
        """
        orig_init = cls.__init__

        @wraps(orig_init)
        def new_init(*args, **kwargs):
            orig_init(*args, **kwargs)
        cls.__init__ = new_init
        valid_aliases = (Request.headers, Request.params,)
        if self.alias not in valid_aliases:
            raise exceptions.InvalidClassDecoChain(self.alias, valid_aliases)
        if self.alias is Request.headers:
            cls.base_headers = self.value
        elif self.alias is Request.params:
            cls.base_params = self.value
        return cls

    def __for_func(self, func: Callable):
        """Wraps a method when it's decorated.  Enables chaining of more than
        one method decorator.  Passes aliases and values set in
        :py:class:`_CommonContext` to :py:class:`Configure.Request` and
        :py:class:`Configure.Response`.
        """
        @wraps(func)
        def arg_handler(*args, **kwargs):
            """Handler for the non-keyword (*args) and keyword (**kwargs)
            arguments that are passed as method parameters.
            """
            connector, config_request, config_response = \
                self.__set_configurables(func, self.__set_args(args), kwargs)
            if self.alias is Request.method:
                return self.__get_message(
                    connector, config_request, config_response)
            return func(
                *(connector, config_request, config_response,), **kwargs)
        return arg_handler

    def __set_configurables(
            self,
            func: Callable,
            args: Tuple[Connector, Configure.Request, Configure.Response],
            kwargs: Dict
    ) -> Tuple[Connector, Configure.Request, Configure.Response]:
        """Assesses the alias assigned to the inherited common context.
        Handles the attribute assignment of an alias and value to either the
        :py:class:`Configure.Request` or :py:class:`Configure.Response`.
        Returns modified non-keyword arguments.
        """
        connector, config_request, config_response = args
        if self.alias is Request.headers:
            config_request.headers.update(self.value)
        elif self.alias is Request.params:
            config_request.params = self.value
        elif self.alias is Response.returns:
            config_response.parameters, config_response.type_ = self.value
        elif self.alias is Request.method:
            config_request.path, config_request.method = self.value
            config_request.signature = signature(func)
            bindings = config_request.signature.bind(
                *(connector,), **kwargs).arguments
            config_request.bindings.update(bindings)
        return connector, config_request, config_response

    @staticmethod
    def __get_message(
            connector: Connector,
            config_request: Configure.Request,
            config_response: Configure.Response
    ) -> Union[ResponseObject, Coroutine]:
        """Assesses the alias assigned to the client type.  Routes to the
        correct message handler based on a blocking or non-blocking client in
        use.
        """
        if connector.client_alias is Client.blocking:
            message = Message.with_requests_client(
                config_request, config_response, connector)
            return message
        if connector.client_alias is Client.nonblocking:
            message = Message.with_aiohttp_client(
                config_request, config_response, connector)
            return message

    @staticmethod
    def __set_args(
            args: Union[
                Tuple[Connector],
                Tuple[Connector, Configure.Request, Configure.Response]]
    ) -> Tuple[Connector, Configure.Request, Configure.Response]:
        """Checks for the existence of :py:class:`Connector`,
        :py:class:`Configure.Request` and :py:class:`Configure.Response`
        objects in the non-keyword arguments (tuple) of a
        method.  If true, returns args.  If false, builds
        :py:class:`Configure.Request` and :py:class:`Configure.Response` and
        returns them along with the existing :py:class:`Connector`.
        """
        if any(isinstance(obj, Connector) for obj in args) and \
           any(isinstance(obj, Configure.Request) for obj in args) and \
           any(isinstance(obj, Configure.Response) for obj in args):
            return args
        return args + (Configure.Request(), Configure.Response(),)


class _Headers(_CommonContext):
    """Template for adding headers to a class or method.
    """

    @typechecked
    def __init__(self, mapping: Dict) -> None:
        super().__init__(Request.headers, mapping)


class _Method(_CommonContext):
    """Template for any HTTP method type to add to an instance method.
    """

    @typechecked
    def __init__(self, path: str) -> None:
        super().__init__(
            Request.method, (path, self.__class__.__name__.upper(),))


class _Params(_CommonContext):
    """Template for adding query parameters to a class or method.
    """

    @typechecked
    def __init__(self, mapping: Dict, encode: bool = False) -> None:
        super().__init__(Request.params, (mapping, encode,))


class _Returns:
    """Namespace for generating the return types f.
    """
    __slots__ = ('json', 'status_code', 'text',)

    def __init__(self) -> None:
        self.json = self._Json
        self.status_code = self._ParametricSimple(Response.status_code)
        self.text = self._ParametricSimple(Response.text)

    class _Json(_CommonContext):
        """Template for the JSON return type.  Allows arguments.
        """

        @typechecked
        def __init__(
                self, key: Optional[Union[List, Tuple, str]] = None) -> None:
            super().__init__(Response.returns, (key, Response.json,))

    class _ParametricSimple(_CommonContext):
        """Template for adding simple return types that do not require
        arguments.
        """

        def __init__(self, type_: Response) -> None:
            super().__init__(Response.returns, (None, type_))


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

There's an optional keyword argument named `encode`.  This is set to `False` by
default.  If set to `True`, this will HTML encode query parameters.  Otherwise,
HTML encoded query parameters can also be explicitly declared. 

::

    @params({'sort': 'asc', 'start_date': '2022-01-01'})
    class Httpbin(Connector):
        ...
        
        @params({'lang': 'en'})
        @get(path='/get')
        def get_(self, **kwargs): pass
"""
returns = _Returns()
"""Provides access to decorators that allow a method to default to returning
JSON, text or status code when invoked.  Declaring a subsequent return type
will overwrite a previous declared return type.

::

    # If the return type is JSON, values can be passed to the `key` argument. 
    # This is not required.  `key` can be of type: `list`, `tuple`, `str` or
    # `None`.
    
    @returns.json(key=...)
    @get(path='/get')
    def get_(self, **kwargs): pass

    # Status code and text return types take no arguments.
    
    @returns.status_code
    @post(path='/post')
    def post_(self, **kwargs): pass
    
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
