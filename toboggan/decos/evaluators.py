# Standard
from inspect import signature
from typing import Any, Callable, Dict, Optional, Tuple, Union, get_type_hints

# Local
from toboggan import Connector
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.models import TypeKwDump, TypeKwObjDump

__all__ = ('_EvalSignature',)


class _EvalSignature:
    __slots__ = ('__eval_type', '__signature',  '__type_hints',)

    def __init__(self, func: Callable):
        self.__signature = signature(func)
        self.__type_hints: Dict = get_type_hints(func)
        self.__eval_type: Any = self.__type_hints.get('return')
    
    @property
    def eval_type(self) -> Optional[Any]:
        return self.__eval_type
    
    def __eval_std(
            self,
            base: TypeKwDump,
            sig_key: Union[Body, Path, Query, QueryKebab, Any],
            sig_value: Union[Dict, str, int]
        ) -> None:
        annotation = self.__type_hints.get(sig_key)
        if annotation in (Body, Path, Query, QueryKebab,):
            base.dump[sig_key] = TypeKwObjDump(
                sig_type=annotation, kw_value=sig_value
            )

    def __eval_options(
            self,
            base: TypeKwDump,
            sig_key: Union[Options, Any],
            sig_value: Union[Dict, str, int]
        ) -> None:
        annotation = self.__type_hints.get(sig_key)
        if annotation is Options and sig_value:
            base.dump[sig_key] = TypeKwObjDump(
                sig_type=annotation, kw_value=sig_value
            )

    def dump(self, *args, **kwargs) -> Tuple[Connector,TypeKwDump]:
        base = TypeKwDump()
        bound = self.__signature.bind(*args, **kwargs)
        bound.apply_defaults()
        conn: Connector = bound.arguments.get('self', Connector)
        for sig_key, sig_value in bound.arguments.items():
            self.__eval_std(base=base, sig_key=sig_key, sig_value=sig_value)
            self.__eval_options(base=base, sig_key=sig_key, sig_value=sig_value)
        return conn, base
