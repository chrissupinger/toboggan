# Standard
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import ClientResponse
from requests import Response

# Local
from .aliases import AliasReqOptType, AliasReturnType, AliasSendsType
from toboggan.connector import Connector

__all__ = (
    # 'InterfaceConnector',
    'InterfaceDecoCommon',
    'InterfaceDecoContext',
    'InterfaceDecoVerb',
    'InterfaceDecoPolymorphic',
    'InterfaceWrappers',
)

class InterfaceDecoPolymorphic(ABC):

    @abstractmethod
    def __init__(self, context: AliasReqOptType, value: Dict) -> None:
        """This is a placeholder."""

    @abstractmethod
    def __call__(
            self,
            callable_: Union[type[Connector], Callable],
            **kwargs
    ) -> Union[type[Connector], Callable]:
        """This is a placeholder."""

    @abstractmethod
    def _for_class(self, cls: type[Connector]) -> type[Connector]:
        """This is a placeholder."""

    @abstractmethod
    def _for_func(self, func: Callable) -> Callable:
        """This is a placeholder."""


class InterfaceDecoCommon(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """This is a placeholder."""


class InterfaceDecoVerb(ABC):

    @abstractmethod
    def __init__(self, path: str) -> None:
        """This is a placeholder."""

    @abstractmethod
    def __call__(self, func: Callable) -> Callable:
        """This is a placeholder."""


class InterfaceDecoContext(ABC):

    @abstractmethod
    def __init__(
            self, context: Union[AliasReturnType, AliasSendsType], **kwargs
    ) -> None:
        """This is a placeholder."""

    @abstractmethod
    def __call__(self, func: Callable, **kwargs) -> Callable:
        """This is a placeholder."""


class InterfaceWrappers(ABC):

    @staticmethod
    @abstractmethod
    def _get_nested(
            json: Optional[Dict],
            value: Optional[Union[str, List[str], Tuple[str]]]
    ) -> Optional[Union[Dict, List, int, str]]:
        """This is a placeholder."""

    @staticmethod
    @abstractmethod
    def _kebabize(key: str) -> str:
        """This is a placeholder."""

    @staticmethod
    @abstractmethod
    def _resolve_options(kw_dump: Dict[str, Dict]) -> Dict:
        """This is a placeholder."""

    @staticmethod
    @abstractmethod
    def _resolve_headers(conn: Connector, ctx_headers_value: Dict) -> Dict:
        """This is a placeholder."""

    @abstractmethod
    def _resolve_query_params(
            self,
            conn: Connector,
            ctx_query_params_value: Dict,
            kw_dump: Dict[str, Dict]
    ) -> Dict:
        """This is a placeholder."""

    @staticmethod
    @abstractmethod
    def _resolve_path_params(kw_dump: Dict[str, Dict], path: str) -> str:
        """This is a placeholder."""

    @staticmethod
    @abstractmethod
    def _resolve_send(
            kw_dump: Dict[str, Dict],
            ctx_sends_type: Optional[AliasSendsType] = None
    ) -> Dict:
        """This is a placeholder."""

    @abstractmethod
    def _resolve_response_sync(
            self,
            response: Response,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None
    ) -> Union[Response, Dict, str, int]:
        """This is a placeholder."""

    @abstractmethod
    async def _resolve_response_async(
            self,
            response: ClientResponse,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None
    ) -> Union[ClientResponse, Dict, str, int]:
        """This is a placeholder."""

    @abstractmethod
    async def wrapper_async(
            self,
            conn: Connector,
            method: str,
            path: str,
            kw_dump: Dict,
            ctx_headers_value: Dict,
            ctx_sends_type: Optional[AliasSendsType] = None,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None,
            **kwargs
    ) -> Union[ClientResponse, Dict, int, str, None]:
        """This is a placeholder."""

    @abstractmethod
    def wrapper_sync(
            self,
            conn: Connector,
            method: str,
            path: str,
            kw_dump: Dict[str, Dict],
            ctx_headers_value: Dict,
            ctx_sends_type: Optional[AliasSendsType] = None,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None,
            **kwargs
    ) -> Union[Response, dict, int, str, None]:
        """This is a placeholder."""
