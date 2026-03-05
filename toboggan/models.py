# Standard
from typing import Dict, List, NamedTuple, Optional, Union

# Local
from toboggan.aliases import AliasReturnType

__all__ = (
    'TypeModuleErrDump',
    'TypeHeadersDump',
    'TypeKwDump',
    'TypeKwObjDump',
    'TypeNestedKeyErrDump',
    'TypeNestedTypeErrDump',
    'TypeQueryParamsDump',
    'TypeRequestSettingsDump',
    'TypeRetryErrDump',
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


class TypeQueryParamsDump(NamedTuple):
    params: Dict


class TypeRetryDump(NamedTuple):
    total: int
    backoff_factor: float
    status_forcelist: list[int]


class TypeRequestSettingsDump(NamedTuple):
    session: object
    method: str
    url: str
    headers: Dict
    query_params: Dict
    send: Union[Dict, str]
    options: Dict
    retry: Optional[TypeRetryDump]
    returns_type: Optional[AliasReturnType]
    returns_json_key: Union[None, str, list[str], tuple[str]]


class TypeSendDataDump(NamedTuple):
    data: Union[Dict, str]


class TypeSendJsonDump(NamedTuple):
    json: Union[Dict, str]


class TypeModuleErrDump(NamedTuple):
    base_dependencies: List[str] = ['requests>=2.25.0']
    optional_dependencies: List[str] = ['aiohttp[speedups]>=3.7.0']
    err_message: str = 'This error occurs when attempting to use an ' \
    'unsupported client type or when a supported client type has not been ' \
    'installed.'
    solution_message: List[str] = [
        'pip install toboggan[aiohttp]', 'OR',
        'pip install toboggan[all]', 'OR',
        'pip install aiohttp[speedups]>=3.7.0', 'OR'
        'pip install aiohttp>=3.7.0'
    ]


class TypeNestedTypeErrDump(NamedTuple):
    type_expected: type
    type_found: type
    err_message: str = 'This error occurs when attempting to coerce a ' \
    'nested key from a type that does not resolve to a dictionary.'
    solution_message: str = 'Double-check the response.  Ensure that the ' \
    'JSON response is a dictionary, '


class TypeNestedKeyErrDump(NamedTuple):
    sequence_expected: list[str]
    sequence_found: list[str]
    err_message: str = 'This error occurs when attempting to coerce a ' \
    'nested key that does not exist in the JSON response.'
    solution_message: str = 'Double-check the response.  Ensure that the ' \
    'key(s) you are attempting to coerce exists in the JSON response.  If ' \
    'the key(s) does/do exist, ensure that the key(s) is/are in the correct ' \
    'order.'


class TypeRetryErrDump(NamedTuple):
    status_code: int
    config: TypeRetryDump
    err_message: str = 'This error occurs when a request fails after ' \
    'exhausting all retry attempts.'
    solution_message: str = 'Consider increasing the number of retry ' \
    'attempts or adjusting the backoff factor to allow for more time ' \
    'between retry attempts.'
