# Standard
from contextvars import ContextVar
from typing import Dict, List, Optional, Tuple, Union

# Local
from toboggan.aliases import AliasReturnType, AliasSendsType
from toboggan.models import TypeRetryDump

__all__ = (
    '_ctx_headers_value',
    '_ctx_query_params_value',
    '_ctx_retry_value',
    '_ctx_returns_json_value',
    '_ctx_returns_type',
    '_ctx_sends_type',
)

_ctx_headers_value: ContextVar[Dict] = ContextVar(
    '_ctx_headers_value', default={}
)
_ctx_query_params_value: ContextVar[Dict] = ContextVar(
    '_ctx_query_params_value', default={}
)
_ctx_retry_value: ContextVar[Optional[TypeRetryDump]] = ContextVar(
    '_ctx_retry_value', default=None
)
_ctx_returns_type: ContextVar[Optional[AliasReturnType]] = ContextVar(
    '_ctx_returns_type', default=None
)
_ctx_returns_json_value: ContextVar[
    Optional[Union[str, List[str], Tuple[str]]]
] = ContextVar(
    '_ctx_returns_json_value', default=None
)
_ctx_sends_type: ContextVar[Optional[AliasSendsType]] = ContextVar(
    '_ctx_sends_type', default=None
)
