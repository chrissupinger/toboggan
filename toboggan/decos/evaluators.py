# Standard
from typing import Any, Callable, Dict, Optional, get_type_hints

# Local
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import TypeKwDump, TypeKwObjDump

__all__ = ('_EvalSignature',)


class _EvalSignature:
    __slots__ = ('__eval_type', '__signature',)

    def __init__(self, func: Callable):
        self.__signature: Dict[str, Any] = get_type_hints(func)
        self.__eval_type = self.__signature.get('return')
    
    @property
    def eval_type(self) -> Optional[Any]:
        return self.__eval_type

    def kw_dump(self, **kwargs) -> TypeKwDump:
        base = TypeKwDump()
        for sig_key, sig_value in self.__signature.items():
            if sig_value in (Body, Path, Query, QueryKebab,):
                base.dump[sig_key] = TypeKwObjDump(
                    sig_type=sig_value, kw_value=kwargs.get(sig_key)
                )
            if sig_value is Options:
                opts = {
                    key: val for key, val in kwargs.items()
                    if key not in base.dump.keys()
                }
                base.dump[sig_key] = TypeKwObjDump(
                    sig_type=sig_value, kw_value=opts
                )
        return base
    