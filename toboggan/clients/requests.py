# Standard
from asyncio import sleep as sleep_async
from time import sleep as sleep_sync
from typing import Any, Dict, List, Optional, Tuple, Union

# Local
from .responses import _resolve_response_awaitable, _resolve_response_std
from .utils import _merge_mappings
from toboggan.aliases import AliasReturnType, AliasSessionType
from toboggan.models import TypeRetryDump, TypeRetryErrDump

__all__ = ('request_async', 'request_sync',)

def request_sync(
        session: Any,
        method: str,
        url: str,
        headers: Dict,
        query_params: Dict,
        send: Dict,
        options: Dict,
        retry: Optional[TypeRetryDump] = None,
        returns_type: Optional[AliasReturnType] = None,
        returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None,
        **kwargs
) -> Union[Any, dict, int, str, None]:
    _merge_mappings(base=headers, supp=options, target='headers')
    _merge_mappings(base=query_params, supp=options, target='params')
    staged_request = lambda: session.request(
        method=method,
        url=url,
        **options,
        **headers,
        **send,
        **query_params,
        **kwargs
    )
    response = staged_request()
    if retry and response.status_code in retry.status_forcelist:
        for attempt in range(retry.total):
            backoff = retry.backoff_factor * (2 ** attempt)
            sleep_sync(backoff)
            if attempt == retry.total - 1:
                err = TypeRetryErrDump(
                    status_code=response.status_code,
                    config=retry
                )
                raise RuntimeError(err)
            response = staged_request()
    resolved_response = _resolve_response_std(
        response=response,
        ctx_returns_type=returns_type,
        ctx_returns_json_key=returns_json_key
    )
    return resolved_response

async def request_async(
        client_type: AliasSessionType,
        session: Any,
        method: str,
        url: str,
        headers: Dict,
        query_params: Dict,
        send: Dict,
        options: Dict,
        retry: Optional[TypeRetryDump] = None,
        returns_type: Optional[AliasReturnType] = None,
        returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None,
        **kwargs
) -> Union[Any, dict, int, str, None]:
    _merge_mappings(base=headers, supp=options, target='headers')
    _merge_mappings(base=query_params, supp=options, target='params')
    staged_request = lambda: session.request(
        method=method,
        url=url,
        **options,
        **headers,
        **send,
        **query_params,
        **kwargs
    )
    response = await staged_request()
    if retry and response.status in retry.status_forcelist:
        for attempt in range(retry.total):
            backoff = retry.backoff_factor * (2 ** attempt)
            await sleep_async(backoff)
            if attempt == retry.total - 1:
                err = TypeRetryErrDump(
                    status_code=response.status,
                    config=retry
                )
                raise RuntimeError(err)
    if client_type is AliasSessionType.AIOHTTP:
        resolved_response = _resolve_response_awaitable(
            response=response,
            ctx_returns_type=returns_type,
            ctx_returns_json_key=returns_json_key
        )
        return await resolved_response
    resolved_response = _resolve_response_std(
        response=response,
        ctx_returns_type=returns_type,
        ctx_returns_json_key=returns_json_key
    )
    return resolved_response
