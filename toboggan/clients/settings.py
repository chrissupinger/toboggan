# Standard
from typing import Any, Dict, List, Optional, Tuple, Union

# Local
from .resolvers import (
    _resolve_headers,
    _resolve_options,
    _resolve_path_params,
    _resolve_query_params,
    _resolve_send,
)
from toboggan.aliases import AliasReturnType, AliasSendsType
from toboggan.models import TypeKwDump, TypeRequestSettingsDump, TypeRetryDump

__all__ = ('Settings',)


class Settings:
    __slots__ = (
        '__base_headers',
        '__base_query_params',
        '__base_url',
        '__ctx_headers_value',
        '__ctx_query_params_value',
        '__ctx_sends_type',
        '__ctx_retry_value',
        '__ctx_returns_type',
        '__ctx_returns_json_key',
        '__kw_dump',
        '__path',
    )

    def __init__(
            self,
            base_url: str,
            path: str,
            base_headers: Dict,
            base_query_params: Dict,
            kw_dump: TypeKwDump,
            ctx_headers_value: Dict,
            ctx_query_params_value: Dict,
            ctx_sends_type: AliasSendsType,
            ctx_retry_value: Optional[TypeRetryDump] = None,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None
    ):
        self.__base_url = base_url
        self.__path = path
        self.__base_headers = base_headers
        self.__base_query_params = base_query_params
        self.__kw_dump = kw_dump
        self.__ctx_retry_value = ctx_retry_value
        self.__ctx_headers_value = ctx_headers_value
        self.__ctx_query_params_value = ctx_query_params_value
        self.__ctx_sends_type = ctx_sends_type
        self.__ctx_returns_type = ctx_returns_type
        self.__ctx_returns_json_key = ctx_returns_json_key

    def url(self) -> str:
        path = _resolve_path_params(self.__kw_dump, self.__path)
        return self.__base_url + path

    def headers(self) -> Dict:
        mapping: Dict = _resolve_headers(
            base_headers=self.__base_headers,
            ctx_headers_value=self.__ctx_headers_value
        )
        return mapping

    def query_params(self) -> Dict:
        mapping: Dict = _resolve_query_params(
            base_query_params=self.__base_query_params,
            ctx_query_params_value=self.__ctx_query_params_value,
            kw_dump=self.__kw_dump
        )
        return mapping

    def send(self) -> Dict:
        type_ = _resolve_send(self.__kw_dump, self.__ctx_sends_type)
        return type_

    def options(self) -> Dict:
        opts: Dict = _resolve_options(self.__kw_dump)
        return opts

    @property
    def retry(self) -> Optional[TypeRetryDump]:
        return self.__ctx_retry_value

    @property
    def returns_type(self) -> Optional[AliasReturnType]:
        return self.__ctx_returns_type

    @property
    def returns_json_key(self) -> Optional[Union[str, List[str], Tuple[str]]]:
        return self.__ctx_returns_json_key

    def dump(
            self, session: Any, method: str
    ) -> TypeRequestSettingsDump:
        return TypeRequestSettingsDump(
            session=session,
            method=method,
            url=self.url(),
            headers=self.headers(),
            query_params=self.query_params(),
            send=self.send(),
            options=self.options(),
            retry=self.retry,
            returns_type=self.returns_type,
            returns_json_key=self.returns_json_key
        )
