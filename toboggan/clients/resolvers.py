# Standard
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party
from requests import Session

try:
    from aiohttp import ClientSession
except ModuleNotFoundError:
    ClientSession = ()

try:
    from httpx import AsyncClient, Client
except ModuleNotFoundError:
    AsyncClient = ()
    Client = ()

# Local
from .utils import _get_nested, _kebabize
from toboggan.aliases import AliasReturnType, AliasSendsType, AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import (
    TypeHeadersDump,
    TypeKwDump,
    TypeModuleErrDump,
    TypeQueryParamsDump,
    TypeSendDataDump,
    TypeSendJsonDump,
)

__all__ = (
    'AsyncClient',
    'Client',
    'ClientSession',
    'Session',
    'resolve_client_type',
    '_resolve_headers',
    '_resolve_options',
    '_resolve_path_params',
    '_resolve_query_params',
    '_resolve_response_async',
    '_resolve_response_sync',
    '_resolve_send',
)

@lru_cache(maxsize=1)
def resolve_client_type(
        session: Optional[Union[Session, ClientSession, AsyncClient, Client]]
) -> AliasSessionType:
    if not session:
        err = TypeModuleErrDump()
        raise ModuleNotFoundError(err)
    if isinstance(session, ClientSession):
        return AliasSessionType.AIOHTTP
    if isinstance(session, AsyncClient):
        return AliasSessionType.HTTPX_ASYNC
    if isinstance(session, Client):
        return AliasSessionType.HTTPX_SYNC
    return AliasSessionType.REQUESTS

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

def _resolve_response_sync(
        response: Any,
        ctx_returns_type: Optional[AliasReturnType] = None,
        ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None
) -> Union[Any, Dict, str, int]:
    if ctx_returns_type is AliasReturnType.JSON:
        json = response.json()
        if ctx_returns_json_key:
            if ctx_returns_json_key:
                return _get_nested(json=json, value=ctx_returns_json_key)
        return json
    elif ctx_returns_type is AliasReturnType.STATUS_CODE:
        return response.status_code
    elif ctx_returns_type is AliasReturnType.TEXT:
        return response.text
    return response

async def _resolve_response_async(
        response: Any,
        ctx_returns_type: Optional[AliasReturnType] = None,
        ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None
) -> Union[Any, Dict, str, int]:
    if ctx_returns_type is AliasReturnType.JSON:
        json = await response.json()
        if ctx_returns_json_key:
            return _get_nested(json=json, value=ctx_returns_json_key)
        return json
    elif ctx_returns_type is AliasReturnType.STATUS_CODE:
        return response.status
    elif ctx_returns_type is AliasReturnType.TEXT:
        return await response.text()
    return response
