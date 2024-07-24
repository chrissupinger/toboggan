# Standard
from inspect import Signature
from typing import ByteString, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import quote_plus

# Third-party
from aiohttp import StreamReader
from multidict import CIMultiDictProxy

# Local
from .aliases import Request, Response
from .annotations import Body, Path, Query, QueryMap
from .connector import Connector

__all__ = ('Configure', 'ResponseObject',)


class Configure:
    """Namespace for generating the settings for requests and responses.
    """

    class Request:
        """Passed as an object across all declared decorators to allow for
        attribute assignment.  Used to build a request's parameters.

        ::

            request = Configure.Request()
            request.* = ...
        """
        __slots__ = (
            'bindings',
            'connector',
            'cookies',
            'data',
            'headers',
            'json',
            'params',
            'path',
            'method',
            'signature',
            'url',)

        def __init__(self):
            self.bindings: Dict = {}
            self.connector: Optional[Connector] = None
            self.cookies: Dict = {}
            self.data: Optional[str] = None
            self.headers: Dict = {}
            self.json: Dict = {}
            self.params: Optional[Tuple[Dict, bool]] = ({}, False,)
            self.path: Optional[str] = None
            self.method: Optional[str] = None
            self.signature: Optional[Signature] = None
            self.url: Optional[str] = None

        def __repr__(self) -> str:
            return \
                f'{self.__class__.__name__}' \
                f'{tuple(f"{ele}={getattr(self, ele)}" for ele in self.__slots__)}'

        @property
        def __pp_path(self) -> str:
            """Formats a path used in as a keyword argument to a method
            decorator.  If the path has a leading of trailing slash, both are
            removed the base path is returned.
            """
            leading = self.path.replace('/', '', 1) \
                if self.path.startswith('/') else self.path
            trailing = leading.rstrip('/') \
                if leading.endswith('/') else leading
            return trailing

        @property
        def __return_annotation(self):
            return self.signature.return_annotation

        @property
        def __settings_data(self) -> Optional[str]:
            data = self.__signature_nested(Body)
            return data if isinstance(data, str) else None

        @property
        def __settings_header(self) -> Dict:
            return {**self.connector.base_headers, **self.headers}

        @property
        def __settings_json(self) -> Optional[Dict]:
            json = self.__signature_nested(Body)
            return json if isinstance(json, Dict) else None

        @property
        def __settings_params(self) -> Dict:
            return {
                **self.__set_params(*self.connector.base_params),
                **self.__set_params(*self.params),
                **self.__set_params(self.__signature_flat(Query)),
                **self.__set_params(self.__signature_nested(QueryMap))}

        @property
        def __settings_url(self) -> str:
            path_params = self.__signature_flat(Path)
            return \
                f'{self.connector.base_url.geturl()}/{self.__pp_path}'.format(**path_params)

        @property
        def settings(self) -> Dict:
            """Dictionary used for configuring a request.

            ::

                # Returns a dictionary
                return {
                    'cookies': ...,
                    'data': ...,
                    'headers': ...,
                    'json': ...,
                    'params': ...,
                    'method': ...,
                    'url': ...
                }

                # Usage with Requests
                prepped = connector.session.prepare_request(
                    Request(**instance.__config_request.settings))

                # Usage with aiohttp
                async with connector.session.request(
                    **instance.__config_request.settings) as response:
                        ...
            """
            return {
                Request.cookies: self.cookies,
                Request.data: self.__settings_data,
                Request.headers: self.__settings_header,
                Request.json: self.__settings_json,
                Request.params: self.__settings_params,
                Request.method: self.method,
                Request.url: self.__settings_url}

        def __get_from_signature(
                self,
                annotation: Union[Body, Path, Query, QueryMap]) -> List[Dict]:
            return [{
                key: self.bindings.get(val.name)} for key, val
                in self.signature.parameters.items()
                if val.annotation is annotation]

        def __signature_flat(self, annotation: Union[Path, Query]) -> Dict:
            """Queries the signature of the method for flat parameters.
            """
            base = {}
            from_signature: List[Optional[Dict]] = \
                self.__get_from_signature(annotation)
            if from_signature:
                for mapping in from_signature:
                    base.update(mapping)
                return base
            return base

        def __signature_nested(self, annotation: Union[Body, QueryMap]):
            """Queries the signature of the method for nested parameters
            (**kwargs).
            """
            from_signature = self.__get_from_signature(annotation)
            if from_signature:
                nested: Dict = next(iter(
                    [val for key, val in next(iter(from_signature)).items()]))
                if (annotation is Body and isinstance(nested, Dict)) or \
                        (annotation is Query):
                    base = {}
                    if nested:
                        base.update(nested)
                        return base
                    return base
                if annotation is Body and isinstance(nested, str):
                    if nested:
                        return nested
                    return None
            return None

        def __set_params(self, value: Dict, encode: bool = False) -> Dict:
            base = {}
            if value:
                if encode:
                    base.update(self.__encode(value))
                    return base
                if not encode:
                    base.update(value)
                    return base
            return base

        @staticmethod
        def __encode(params: Union[Dict, str]) -> Union[Dict, str]:
            if isinstance(params, Dict):
                return {key: quote_plus(val) for key, val in params.items()}
            if isinstance(params, str):
                return quote_plus(params)

    class Response:
        """Passed as an object across all declared decorators to allow for
        attribute assignment.  Used to pass response requirements when as
        determined by a `returns.*` decoration of a method.

        ::

            response = Configure.Response()
            response.* = ...
        """
        __slots__ = ('parameters', 'type_',)

        def __init__(self):
            self.parameters: Optional[Union[List, Tuple, str]] = None
            self.type_: Optional[Response] = None

        def __repr__(self) -> str:
            return \
                f'{self.__class__.__name__}' \
                f'{tuple(f"{ele}={getattr(self, ele)}" for ele in self.__slots__)}'


class ResponseObject:
    """Enables object access parity regardless of client type response
    received.

    ::

        response = ResponseObject(**kwargs)

    References:
        - aiohttp: :py:class:`aiohttp.ClientResponse`
        - Requests: :py:class:`requests.Response`
    """
    __slots__ = (
        '__json',
        '__raise_for_status',
        'content',
        'encoding',
        'headers',
        'history',
        'ok',
        'status_code',
        'text',)

    def __init__(
            self,
            content: Union[ByteString, StreamReader],
            encoding: str,
            headers: Union[CIMultiDictProxy, Dict],
            history: Union[List, Tuple],
            json: Dict,
            ok: bool,
            raise_for_status: Callable,
            status_code: int,
            text: str) -> None:
        self.__json = json
        self.__raise_for_status = raise_for_status
        self.content = content
        self.encoding = encoding
        self.headers = headers
        self.history = history
        self.ok = ok
        self.status_code = status_code
        self.text = text

    def json(self, **kwargs) -> Dict:
        return self.__json

    def raise_for_status(self):
        return self.__raise_for_status()
