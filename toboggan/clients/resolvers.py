# Standard
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

# Third-party
from requests import Session

# Local
from toboggan.aliases import AliasReturnType, AliasSendsType, AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import (
    TypeModuleErrDump,
    TypeHeadersDump,
    TypeKwDump,
    TypeNestedKeyErrDump,
    TypeNestedTypeErrDump,
    TypeQueryParamsDump,
    TypeRequestSettingsDump,
    TypeRetryDump,
    TypeSendDataDump,
    TypeSendJsonDump,
)

__all__ = (
    '_get_nested', '_merge_mappings', 'ResolverRequest', 'resolve_client_type',
)

def resolve_client_type(session: Any) -> Optional[AliasSessionType]:
    if isinstance(session, Session):
        return AliasSessionType.REQUESTS
    try:
        from aiohttp import ClientSession
        if isinstance(session, ClientSession):
            return AliasSessionType.AIOHTTP
    except ModuleNotFoundError:
        err = TypeModuleErrDump()
        raise ModuleNotFoundError(err)

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
            except TypeError:
                 err = TypeNestedTypeErrDump(
                    type_expected=dict,
                    type_found=type(json)
                 )
                 raise TypeError(err)
            except KeyError:
                err = TypeNestedKeyErrDump(
                    sequence_expected=list(value),
                    sequence_found=list(orig.keys())
                )
                raise KeyError(err)
    return json

def _merge_mappings(
        base: Dict, supp: Dict, target: Literal['headers', 'params']
) -> None:
    common_keys = base.keys() & supp.keys()
    if common_keys:
        for key in common_keys:
            base.get(target).update(supp[key])
        supp.pop(target, None)

def _kebabize(key: str) -> str:
        return key.replace('_', '-')

def _resolve_options(kw_dump: TypeKwDump) -> Dict:
        for _, val in kw_dump.dump.items():
            if val.sig_type is Options and val.kw_value:
                return val.kw_value
        return {}

def _resolve_headers(base_headers: Dict, ctx_headers_value: Dict) -> Dict:
        base = {}
        base.update(base_headers)
        base.update(ctx_headers_value)
        return TypeHeadersDump(base)._asdict() if base else {}

def _resolve_path_params(kw_dump: TypeKwDump, path: str) -> str:
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

def _resolve_send(
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

def _resolve_query_params(
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
                base[_kebabize(key)] = val.kw_value
        if base:
            return TypeQueryParamsDump(base)._asdict()
        return base


class ResolverRequest:
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
            ctx_returns_json_key: Optional[
                Union[str, List[str], Tuple[str]]
            ] = None
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

    def settings_dump(
            self, session: Session, method: str
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