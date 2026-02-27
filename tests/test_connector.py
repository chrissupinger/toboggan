# Test
from pytest import mark

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from toboggan import Connector
from toboggan.aliases import AliasSessionType

def test_session_requests():
    connector = Connector()
    assert isinstance(connector.session(), Session)

def test_client_type_alias_requests():
    connector = Connector()
    assert connector.client_type is AliasSessionType.REQUESTS

@mark.asyncio
async def test_session_aiohttp():
    connector = Connector(client=ClientSession())
    async with connector.session() as session:
        assert isinstance(session, ClientSession)

@mark.asyncio
async def test_client_type_alias_aiohttp():
    connector = Connector(client=ClientSession())
    assert connector.client_type is AliasSessionType.AIOHTTP
