# Third-party
from pytest import fixture, mark
from aiohttp import ClientSession
from requests import Session

# Local
from toboggan import Connector, headers, params
from toboggan.aliases import AliasSessionType

@fixture
def connector_requests():
    return Connector(base_url='https://httpbin.org/')

def test_session_requests(connector_requests):
    assert isinstance(connector_requests.session(), Session)

def test_base_url_requests(connector_requests):
    assert connector_requests.base_url == 'https://httpbin.org/'

def test_client_type_alias_requests(connector_requests):
    assert connector_requests.client_type is AliasSessionType.REQUESTS

@fixture
@mark.asyncio
async def connector_aiohttp():
    return Connector(base_url='https://httpbin.org/', client=ClientSession())

@mark.asyncio
async def test_session_aiohttp(connector_aiohttp):
    async with connector_aiohttp.session() as session:
        assert isinstance(session, ClientSession)

@mark.asyncio
async def test_base_url_aiohttp(connector_aiohttp):
    assert connector_aiohttp.base_url == 'https://httpbin.org/'

@mark.asyncio
async def test_client_type_alias_aiohttp(connector_aiohttp):
    assert connector_aiohttp.client_type is AliasSessionType.AIOHTTP


@params({'limit': 10})
@headers({'User-Agent': 'toboggan'})
class HttpBin(Connector):

    def __init__(self, base_url: str = 'http://httpbin.org/') -> None:
        super().__init__(base_url=base_url)


@fixture
def fixture_api():
    return HttpBin()

def test_base_headers(fixture_api):
    assert fixture_api.base_headers == {'User-Agent': 'toboggan'}

def test_base_query_params(fixture_api):
    assert fixture_api.base_query_params == {'limit': 10}
