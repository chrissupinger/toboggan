# Standard
from inspect import getmembers, isawaitable, iscoroutinefunction
from typing import Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import ClientResponse, client_exceptions
from requests import Request

# Local
from .aliases import Response
from .connector import Connector
from .models import Configure, ResponseObject

__all__ = ('Message',)


class Message:

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
                Request(**instance.__config_request.settings))
            response = connector.session.send(prepped)
            return ResponseObject(
                response.content,
                response.encoding,
                response.headers,
                response.history,
                response.json(),
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
