# Standard
from typing import Dict, List, Literal, Optional, Tuple, Union

# Local
from toboggan.models import TypeNestedKeyErrDump, TypeNestedTypeErrDump

__all__ = ('_get_nested', '_kebabize', '_merge_mappings',)

def _get_nested(
        json: Dict,
        value: Union[str, List[str], Tuple[str]]
) -> Optional[Union[Dict, List, int, str]]:
    orig = json
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
