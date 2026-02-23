# Standard
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

# Local
from .aliases import AliasSendsType, AliasReturnType
from .connector import Connector

__all__ = (
    'TypeHeadersDump',
    'TypeKwDump',
    'TypeNestedDump',
    'TypeQueryParams',
    'TypeSendDataDump',
    'TypeSendJsonDump',
    'TypeWrapperMapping',
)


class TypeHeadersDump(NamedTuple):
    headers: Dict[str, str]


class TypeKwDump(NamedTuple):
    sig_type: type
    kw_value: Union[str, int]


class TypeNestedDump(NamedTuple):
    sequence_expected: list[str]
    sequence_found: list[str]


class TypeQueryParams(NamedTuple):
    params: Dict


class TypeSendDataDump(NamedTuple):
    data: Union[Dict, str]


class TypeSendJsonDump(NamedTuple):
    json: Union[Dict, str]


class TypeWrapperMapping(NamedTuple):
    conn: Connector
    method: str
    path: str
    kw_dump: Dict[str, Dict]
    ctx_headers_value: Dict
    ctx_query_params_value: Dict
    ctx_sends_type: Optional[AliasSendsType]
    ctx_returns_type: Optional[AliasReturnType]
    ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]]
