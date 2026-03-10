# Standard
from functools import lru_cache
from typing import Optional, Tuple

# Third-party
try:
    from pydantic import VERSION
except ModuleNotFoundError:
    VERSION = '0'

# Local
from toboggan.aliases import AdaptersEvalType


__all__ = ('eval_adapters',)

@lru_cache(maxsize=1)
def _resolve_eval_adapters() -> Tuple[AdaptersEvalType]:
    base = []
    if VERSION.startswith('2'):
        base.append(AdaptersEvalType.PYDANTIC_V2)
    elif VERSION.startswith('1'):
        base.append(AdaptersEvalType.PYDANTIC_V1)
    return tuple(base)

eval_adapters: Tuple[Optional[AdaptersEvalType]] = _resolve_eval_adapters()
