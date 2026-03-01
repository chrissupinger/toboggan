# Local
from toboggan import Body, Options, Path, Query
from toboggan.models import TypeKwDump, TypeKwObjDump
from toboggan.clients.resolvers import (
    _get_nested,
    _kebabize,
    _merge_mappings,
    _resolve_headers,
    _resolve_options,
    _resolve_path_params,
    _resolve_query_params,
    _resolve_send,
)

def test_get_nested():
    json = {'a': {'b': {'c': 1}}}
    assert _get_nested(json, 'a') == {'b': {'c': 1}}
    assert _get_nested(json, ['a', 'b']) == {'c': 1}
    assert _get_nested(json, ['a', 'b', 'c']) == 1

def test_kebabize():
    assert _kebabize('test_key') == 'test-key'

def test_merge_mappings():
    base = {'params': {'a': 1, 'b': 2}}
    supp = {'params': {'b': 3, 'c': 4}}
    _merge_mappings(base=base, supp=supp, target='params')
    assert base == {'params': {'a': 1, 'b': 3, 'c': 4}}
    assert supp == {}

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
