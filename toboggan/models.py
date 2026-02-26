# Standard
from typing import Dict, NamedTuple, Union

__all__ = (
    'TypeHeadersDump',
    'TypeKwDump',
    'TypeKwObjDump',
    'TypeNestedDump',
    'TypeQueryParams',
    'TypeSendDataDump',
    'TypeSendJsonDump',
)


class TypeHeadersDump(NamedTuple):
    headers: Dict[str, str]


class TypeKwObjDump(NamedTuple):
    sig_type: type
    kw_value: Union[Dict, str, int]


class TypeKwDump(NamedTuple):
    dump: Dict = {}


class TypeNestedDump(NamedTuple):
    sequence_expected: list[str]
    sequence_found: list[str]


class TypeQueryParams(NamedTuple):
    params: Dict


class TypeSendDataDump(NamedTuple):
    data: Union[Dict, str]


class TypeSendJsonDump(NamedTuple):
    json: Union[Dict, str]
