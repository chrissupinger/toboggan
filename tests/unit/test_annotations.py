# Local
from toboggan import Body, Options, Path, Query, QueryKebab

def test_annotations():
    assert Body({'hello': 'world'}) == {'hello': 'world'}
    assert Options({'timeout': 5}) == {'timeout': 5}
    assert Path('/api/v1/resource') == '/api/v1/resource'
    assert Query('limit') == 'limit'
    assert QueryKebab('sort-by') == 'sort-by'
