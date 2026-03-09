# Third-party
from pytest import fixture, mark, raises
from aiohttp import ClientSession
from httpx import AsyncClient, Client
from requests import Session

# Local
from toboggan import Body, Options, Path, Query
from toboggan.aliases import AliasSessionType
from toboggan.models import TypeKwDump, TypeKwObjDump
from toboggan.clients.resolvers import (
    resolve_client_type,
    _resolve_headers,
    _resolve_options,
    _resolve_path_params,
    _resolve_query_params,
    _resolve_send,
)

@fixture
def test_resolve_client_type():
    return resolve_client_type

def test_client_type_requests(test_resolve_client_type):
    assert test_resolve_client_type(Session()) == AliasSessionType.REQUESTS

@mark.asyncio
async def test_client_type_aiohttp(test_resolve_client_type):
    assert test_resolve_client_type(ClientSession()) == AliasSessionType.AIOHTTP

def test_client_type_httpx_sync(test_resolve_client_type):
    assert test_resolve_client_type(Client()) == AliasSessionType.HTTPX_SYNC

@mark.asyncio
async def test_client_type_httpx_async(test_resolve_client_type):
    assert test_resolve_client_type(AsyncClient()) == AliasSessionType.HTTPX_ASYNC

def test_client_type_none(test_resolve_client_type):
    with raises(ModuleNotFoundError):
        test_resolve_client_type(None)

def test_resolve_headers():
    base = {'Content-Type': 'application/json'}
    ctx_headers_value = {'User-Agent': 'toboggan'}
    assert _resolve_headers(base, ctx_headers_value) == {
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'toboggan'
        }
    }

def test_resolve_options():
    kw_dump = TypeKwDump(dump={
        'options': TypeKwObjDump(
            sig_type=Options,
            kw_value={'timeout': 5}
        )
    })
    assert _resolve_options(kw_dump) == {'timeout': 5}

def test_resolve_path_params():
    kw_dump = TypeKwDump(dump={
        'first_path': TypeKwObjDump(sig_type=Path, kw_value='hello'),
        'second_path': TypeKwObjDump(sig_type=Path, kw_value='world')
    })
    path = 'anything/{first_path}/{second_path}'
    assert _resolve_path_params(kw_dump, path) == 'anything/hello/world'

def test_resolve_query_params():
    base_query_params = {'a': 1}
    ctx_query_params_value = {'b': 2}
    kw_dump = TypeKwDump(dump={
        'c': TypeKwObjDump(sig_type=Query, kw_value='3')
    })
    assert _resolve_query_params(base_query_params, ctx_query_params_value, kw_dump) == {
        'params': {
            'a': 1,
            'b': 2,
            'c': '3'
        }
    }

def test_resolve_send():
    kw_dump = TypeKwDump(dump={
        'body': TypeKwObjDump(sig_type=Body, kw_value={'key': 'value'})
    })
    assert _resolve_send(kw_dump) == {'json': {'key': 'value'}}
