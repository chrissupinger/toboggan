# Standard
from functools import wraps
from inspect import (
    getmembers,
    isawaitable,
    isclass,
    iscoroutinefunction,
    isfunction,
    signature,)
from typing import Callable, Coroutine, Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import ClientResponse, client_exceptions
from requests import Request as SyncRequest, exceptions
from typeguard import typechecked

# Local
from . import exceptions
from .aliases import Client, Request, Response, Send
from .connector import Connector
from .models import Configure, ResponseObject

__all__ = ('ParametricComplex', 'ParametricSimple',)


class _Message:

    class Request:

        def __init__(
                self, config_request: Configure.Request, connector: Connector):
            self.__config_request = config_request
            self.__config_request.connector = connector

        @classmethod
        def by_requests_client(
                cls,
                config_request: Configure.Request,
                connector: Connector) -> ResponseObject:
            instance = cls(config_request, connector)
            prepped = connector.session.prepare_request(
                SyncRequest(**instance.__config_request.settings))
            response = connector.session.send(prepped)
            try:
                response_json = response.json()
            except exceptions.JSONDecodeError as message:
                response_json = {'error': message}
            return ResponseObject(
                response.content,
                response.encoding,
                response.headers,
                response.history,
                response_json,
                response.ok,
                response.raise_for_status,
                response.status_code,
                response.text)

        @classmethod
        async def by_aiohttp_client(
                cls,
                config_request: Configure.Request,
                connector: Connector) -> ResponseObject:
            instance = cls(config_request, connector)
            async with connector.session.request(
                    **instance.__config_request.settings) as response:
                try:
                    response_json = await response.json()
                except client_exceptions.ContentTypeError as message:
                    response_json = {'error': message}
                return ResponseObject(
                    response.content,
                    response.get_encoding(),
                    response.headers,
                    response.history,
                    response_json,
                    response.ok,
                    response.raise_for_status,
                    response.status,
                    await response.text())

        @staticmethod
        def __get_awaitables(response: ClientResponse) -> List:
            """If used on a :py:class:`ClientResponse` without the filters,
            this should return an iterable that contains: `json`, `read`,
            `start`, `text` and `wait_for_close`.  With filters, it removes
            `start` and `wait_for_close` from the iterable.

            Inverse::

                return [
                    name for name, value in getmembers(response)
                    if not name.startswith('_')
                    and not iscoroutinefunction(value)
                    and not isawaitable(value)]
            """
            return [
                name for name, value in getmembers(response)
                if not name.startswith('_')
                and name not in ('start', 'wait_for_close',)
                and iscoroutinefunction(value) or isawaitable(value)]

    class Response:

        def __init__(
                self,
                config_response: Configure.Response,
                message: ResponseObject):
            self.__config_response = config_response
            self.__message = message

        @staticmethod
        def __get_nested(
                json: Dict,
                key: Union[List, Tuple, str]
        ) -> Optional[Union[Dict, List, int, str]]:
            iterable_ = (key,) if isinstance(key, str) else key
            for index in iterable_:
                try:
                    json = json[index]
                except KeyError:
                    return None
            return json

        @classmethod
        def from_client(
                cls,
                config_response: Configure.Response,
                message: ResponseObject
        ) -> Union[ResponseObject, Dict, List, int, str]:
            if config_response.type_:
                if config_response.type_ is Response.json:
                    json = message.json()
                    if config_response.parameters:
                        nested = cls.__get_nested(
                            json, config_response.parameters)
                        return nested
                    return json
                if config_response.type_ is Response.status_code:
                    return message.status_code
                if config_response.type_ is Response.text:
                    return message.text
            return message

    @classmethod
    def with_requests_client(
            cls,
            config_request: Configure.Request,
            config_response: Configure.Response,
            connector: Connector) -> ResponseObject:
        response = cls.Response.from_client(
            config_response,
            cls.Request.by_requests_client(config_request, connector))
        return response

    @classmethod
    async def with_aiohttp_client(
            cls,
            config_request: Configure.Request,
            config_response: Configure.Response,
            connector: Connector) -> ResponseObject:
        response = cls.Response.from_client(
            config_response,
            await cls.Request.by_aiohttp_client(config_request, connector))
        return response


class _CommonContext:
    """The common context shared across every class-level and method-level
    decorator.
    """
    __slots__ = ('alias', 'value',)

    @typechecked
    def __init__(
            self,
            alias: Union[Request, Response, Send],
            value: Optional[Tuple]) -> None:
        self.alias = alias
        self.value = value

    def __repr__(self) -> str:
        return \
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
            cls.base_headers = next(iter(self.value))
        elif self.alias is Request.params:
            cls.base_params = next(iter(self.value))
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
            config_request.headers.update(next(iter(self.value)))
        elif self.alias is Request.params:
            config_request.params = next(iter(self.value))
        elif self.alias is Request.send_format:
            config_request.send_format = next(iter(self.value))
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
            message = _Message.with_requests_client(
                config_request, config_response, connector)
            return message
        if connector.client_alias is Client.nonblocking:
            message = _Message.with_aiohttp_client(
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


class ParametricSimple(_CommonContext):
    """Template for adding simple return types that do not require
    arguments.
    """

    def __init__(
            self,
            alias: Union[Request, Response, Send],
            value: Optional[Tuple] = None) -> None:
        super().__init__(alias=alias, value=value)


class ParametricComplex(_CommonContext):

    def __init__(
            self, alias: Union[Request, Response, Send], value: Tuple) -> None:
        super().__init__(alias=alias, value=value)

    def __call__(
            self,
            callable_: Callable = None,
            **kwargs) -> Callable:
        if not callable_:
            return self.__class__(**kwargs)
        return super().__call__(callable_)
