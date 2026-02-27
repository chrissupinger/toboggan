# Standard
from typing import Dict, NamedTuple, Optional, Union

# Local
from toboggan.aliases import AliasReturnType

__all__ = (
    'TypeHeadersDump',
    'TypeKwDump',
    'TypeKwObjDump',
    'TypeNestedDump',
    'TypeQueryParams',
    'TypeRequestSettings',
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


class TypeRequestSettings(NamedTuple):
    session: object
    method: str
    url: str
    headers: Dict
    query_params: Dict
    send: Union[Dict, str]
    options: Dict
    returns_type: Optional[AliasReturnType]
    returns_json_key: Union[None, str, list[str], tuple[str]]


class TypeSendDataDump(NamedTuple):
    data: Union[Dict, str]


class TypeSendJsonDump(NamedTuple):
    json: Union[Dict, str]
