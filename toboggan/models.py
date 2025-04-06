# Standard
from inspect import Signature
from typing import ByteString, Callable, Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import StreamReader
from multidict import CIMultiDictProxy

# Local
from .aliases import Request, Response, Send
from .annotations import Body, Path, Query, QueryKebab, QueryMap, QueryMapKebab
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
            'send_format',
            'signature',
            'url',)

        def __init__(self):
            self.bindings: Dict = {}
            self.connector: Optional[Connector] = None
            self.cookies: Dict = {}
            self.data: Optional[str] = None
            self.headers: Dict = {}
            self.json: Optional[Dict] = None
            self.params: Dict = {}
            self.path: Optional[str] = None
            self.method: Optional[str] = None
            self.signature: Optional[Signature] = None
            self.url: Optional[str] = None
            self.send_format: Optional[Send] = None

        def __repr__(self) -> str:
            return \
                f'{self.__class__.__name__}' \
                f'{tuple(f"{ele}={getattr(self, ele)}" for ele in self.__slots__)}'

        @property
        def __pp_path(self) -> str:
            """Formats a path used in as a keyword argument to a method
            decorator.  If the path has a leading of trailing slash, both are
            removed and the base path is returned.
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
            if data:
                if self.send_format is Send.data:
                    return data
                if self.send_format is Send.json:
                    return None
                if isinstance(data, str):
                    return data
            return None

        @property
        def __settings_header(self) -> Dict:
            return {**self.connector.base_headers, **self.headers}

        @property
        def __settings_json(self) -> Optional[Dict]:
            json = self.__signature_nested(Body)
            if json:
                if self.send_format is Send.data:
                    return None
                if self.send_format is Send.json:
                    return json
                if isinstance(json, Dict):
                    return json
            return None

        @property
        def __settings_params(self) -> Dict:
            return {
                **self.connector.base_params,
                **self.params,
                **self.__signature_flat(Query),
                **self.__signature_flat(QueryKebab),
                **self.__signature_nested(QueryMap),
                **self.__signature_nested(QueryMapKebab)}

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
                annotation: Union[
                    Body, Path, Query, QueryKebab, QueryMap, QueryMapKebab]
        ) -> List[Dict]:
            base = []
            for key, val in self.signature.parameters.items():
                if val.annotation is annotation:
                    base.append({key: self.bindings.get(val.name)})
            return base

        def __signature_flat(
                self, annotation: Union[Path, Query, QueryKebab]
        ) -> Dict:
            """Queries the signature of the method for flat parameters.
            """
            base = {}
            from_signature: List[Optional[Dict]] = \
                self.__get_from_signature(annotation)
            if from_signature:
                for mapping in from_signature:
                    if annotation in (Query, QueryKebab,):
                        if annotation is QueryKebab:
                            mapping = self.__kebabize(mapping)
                        base.update(mapping)
                    else:
                        base.update(mapping)
                return base
            return base

        def __signature_nested(
                self, annotation: Union[Body, QueryMap, QueryMapKebab]
        ) -> Union[Dict, str, None]:
            """Queries the signature of the method for nested parameters
            (**kwargs).
            """
            base = {}
            from_signature = self.__get_from_signature(annotation)
            if from_signature:
                nested: Dict = next(iter(
                    [val for key, val in next(iter(from_signature)).items()]))
                if nested:
                    if isinstance(nested, Dict):
                        if annotation in (Body, QueryMap, QueryMapKebab,):
                            if annotation is QueryMapKebab:
                                nested = self.__kebabize(nested)
                            base.update(nested)
                            return base
                        return base
                    if isinstance(nested, str):
                        if annotation is Body:
                            return nested
                        return None
            return base

        @staticmethod
        def __kebabize(params: Union[Dict, str]) -> Union[Dict, str]:
            return {key.replace('_', '-'): val for key, val in params.items()}

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
    """Enables near parity and object access regardless of client type response
    received.  Additional callables, from both library response objects,
    should be considered for relevancy in the future.

    ::

        response = ResponseObject(**kwargs)
        response.content
        response.encoding
        response.headers
        response.history
        response.json()
        response.ok
        response.raise_for_status()
        response.status_code
        response.text

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
