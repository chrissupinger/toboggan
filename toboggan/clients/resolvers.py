# Standard
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

# Third-party
from requests import Session

# Local
from toboggan.aliases import AliasReturnType, AliasSendsType, AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import (
    TypeHeadersDump,
    TypeKwDump,
    TypeNestedDump,
    TypeQueryParams,
    TypeRequestSettings,
    TypeSendDataDump,
    TypeSendJsonDump,
)

__all__ = (
    '_get_nested', '_merge_mappings', 'ResolverRequest', 'resolve_client_type',
)

def resolve_client_type(session: Any) -> AliasSessionType:
    if isinstance(session, Session):
        return AliasSessionType.REQUESTS
    try:
        from aiohttp import ClientSession
        if isinstance(session, ClientSession):
            return AliasSessionType.AIOHTTP
    except ModuleNotFoundError:
        raise ModuleNotFoundError()
    return AliasSessionType.NONE

def _get_nested(
        json: Optional[Dict],
        value: Optional[Union[str, List[str], Tuple[str]]]
) -> Optional[Union[Dict, List, int, str]]:
    orig = json
    if json and value:
        keys = (value,) if isinstance(value, str) else value
        for key in keys:
            try:
                json = json[key]
            except (KeyError, TypeError,):
                return TypeNestedDump(
                    sequence_expected=list(value),
                    sequence_found=list(orig.keys())
                )._asdict()
    return json

def _merge_mappings(
        base: Dict, supp: Dict, target: Literal['headers', 'params']
) -> None:
    common_keys = base.keys() & supp.keys()
    if common_keys:
        for key in common_keys:
            base.get(target).update(supp[key])
        supp.pop(target, None)


class ResolverRequest:
    __slots__ = (
        '__base_headers',
        '__base_query_params',
        '__base_url',
        '__ctx_headers_value',
        '__ctx_query_params_value',
        '__ctx_sends_type',
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
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None
    ):
        self.__base_url = base_url
        self.__path = path
        self.__base_headers = base_headers
        self.__base_query_params = base_query_params
        self.__kw_dump = kw_dump
        self.__ctx_headers_value = ctx_headers_value
        self.__ctx_query_params_value = ctx_query_params_value
        self.__ctx_sends_type = ctx_sends_type
        self.__ctx_returns_type = ctx_returns_type
        self.__ctx_returns_json_key = ctx_returns_json_key

    @staticmethod
    def __kebabize(key: str) -> str:
        return key.replace('_', '-')

    @staticmethod
    def __resolve_options(kw_dump: TypeKwDump) -> Dict:
        for key, val in kw_dump.dump.items():
            if val.sig_type is Options and val.kw_value:
                return val.kw_value
        return {}

    @staticmethod
    def __resolve_headers(base_headers: Dict, ctx_headers_value: Dict) -> Dict:
        base = {}
        base.update(base_headers)
        base.update(ctx_headers_value)
        return TypeHeadersDump(base)._asdict() if base else {}

    @staticmethod
    def __resolve_path_params(kw_dump: TypeKwDump, path: str) -> str:
        params = [
            {key: val.kw_value} for key, val in kw_dump.dump.items()
            if val.sig_type is Path and val.kw_value
        ]
        if params:
            resolved = {}
            for param in params:
                resolved.update(param)
            return path.format(**resolved)
        return path

    @staticmethod
    def __resolve_send(
            kw_dump: TypeKwDump,
            ctx_sends_type: Optional[AliasSendsType] = None
    ) -> Dict:
        body = next(
            (obj for obj in kw_dump.dump.values() if obj.sig_type is Body),
            None
        )
        if body:
            if ctx_sends_type and ctx_sends_type is AliasSendsType.DATA:
                return TypeSendDataDump(body.kw_value)._asdict()
            return TypeSendJsonDump(body.kw_value)._asdict()
        return {}

    def __resolve_query_params(
            self,
            base_query_params: Dict,
            ctx_query_params_value: Dict,
            kw_dump: TypeKwDump
    ) -> Dict:
        base = {}
        base.update(base_query_params)
        base.update(ctx_query_params_value)
        for key, val in kw_dump.dump.items():
            if val.sig_type is Query and val.kw_value:
                base[key] = val.kw_value
            elif val.sig_type is QueryKebab and val.kw_value:
                base[self.__kebabize(key)] = val.kw_value
        if base:
            return TypeQueryParams(base)._asdict()
        return base

    def url(self) -> str:
        path = self.__resolve_path_params(self.__kw_dump, self.__path)
        return self.__base_url + path

    def headers(self) -> Dict:
        mapping: Dict = self.__resolve_headers(
            base_headers=self.__base_headers,
            ctx_headers_value=self.__ctx_headers_value
        )
        return mapping

    def query_params(self) -> Dict:
        mapping: Dict = self.__resolve_query_params(
            base_query_params=self.__base_query_params,
            ctx_query_params_value=self.__ctx_query_params_value,
            kw_dump=self.__kw_dump
        )
        return mapping

    def send(self) -> Dict:
        type_ = self.__resolve_send(self.__kw_dump, self.__ctx_sends_type)
        return type_

    def options(self) -> Dict:
        opts: Dict = self.__resolve_options(self.__kw_dump)
        return opts

    @property
    def returns_type(self) -> Optional[AliasReturnType]:
        return self.__ctx_returns_type

    @property
    def returns_json_key(self) -> Optional[Union[str, List[str], Tuple[str]]]:
        return self.__ctx_returns_json_key

    def settings_dump(
            self, session: Session, method: str
        ) -> TypeRequestSettings:
        return TypeRequestSettings(
            session=session,
            method=method,
            url=self.url(),
            headers=self.headers(),
            query_params=self.query_params(),
            send=self.send(),
            options=self.options(),
            returns_type=self.returns_type,
            returns_json_key=self.returns_json_key
        )