# Standard
from functools import lru_cache
from typing import Dict, Optional, Union

# Third-party
from requests import Session

# Local
from .utils import _kebabize
from toboggan.aliases import AliasSendsType, AliasSessionType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import (
    TypeHeadersDump,
    TypeKwDump,
    TypeClientModuleErrDump,
    TypeQueryParamsDump,
    TypeSendDataDump,
    TypeSendJsonDump,
)


class __NoClientModule:
    err = TypeClientModuleErrDump()


try:
    from aiohttp import ClientSession
except ModuleNotFoundError:
    ClientSession = __NoClientModule

try:
    from httpx import AsyncClient, Client
except ModuleNotFoundError:
    AsyncClient = __NoClientModule
    Client = __NoClientModule

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
    '_resolve_send',
)

@lru_cache(maxsize=1)
def resolve_client_type(
        session: Optional[Union[Session, ClientSession, AsyncClient, Client]]
) -> AliasSessionType:
    if not isinstance(session, (Session, ClientSession, AsyncClient, Client,)):
        raise ModuleNotFoundError(__NoClientModule.err)
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
