# Local
from toboggan.clients.utils import _get_nested, _kebabize, _merge_mappings

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
