# Standard
from typing import Any, Dict, List, Optional, Tuple, Union

# Local
from .utils import _get_nested
from toboggan.aliases import AliasReturnType

__all__ = ('_resolve_response_awaitable', '_resolve_response_std',)

def _resolve_response_std(
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

async def _resolve_response_awaitable(
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
