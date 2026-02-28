# Third-party
from pytest import fixture, mark
from aiohttp import ClientSession
from requests import Session

# Local
from toboggan import Connector
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
