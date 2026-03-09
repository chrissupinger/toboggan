# Standard
from asyncio import gather
from typing import Dict

# Third-party
from pytest import fixture, mark
from aiohttp import ClientSession

# Local
from toboggan import Body, Connector, Path, get, post, returns, sends


class HttpBin(Connector):

    def __init__(self, base_url: str = 'http://httpbin.org/') -> None:
        super().__init__(base_url=base_url)

    @returns.json
    @get(path='anything')
    def method_get(self):
        pass

    @returns.json
    @get(path='anything/{first_path}/{second_path}')
    def method_get_path_params(self, first_path: Path, second_path: Path):
        pass
    
    @returns.json
    @sends.json
    @post(path='anything')
    def method_post_json(self, body: Body):
        pass
    
    @returns.json
    @sends.form_url_encoded
    @post(path='anything')
    def method_post_form_url_encoded(self, body: Body):
        pass


@fixture
@mark.asyncio
async def fixture_api():
    httpbin = HttpBin()
    return httpbin(client=ClientSession())

@fixture
@mark.asyncio
async def fixture_get(fixture_api):
    async with fixture_api.session():
        return await fixture_api.method_get()

@mark.asyncio
async def test_get_json(fixture_get):
    assert isinstance(fixture_get, Dict)

@fixture
@mark.asyncio
async def fixture_get_path_params(fixture_api):
    async with fixture_api.session():
        return await fixture_api.method_get_path_params(
            first_path='hello', second_path='world'
        )

@mark.asyncio
async def test_get_path_params(fixture_get_path_params):
    response = fixture_get_path_params
    assert response.get('url') == 'http://httpbin.org/anything/hello/world'

@fixture
@mark.asyncio
async def fixture_post_json(fixture_api):
    async with fixture_api.session():
        return await fixture_api.method_post_json(body={'Hello': 'World!'})

@mark.asyncio
async def test_post_json(fixture_post_json):
    response = fixture_post_json
    assert isinstance(response.get('json'), Dict)
    assert response.get('json') == {'Hello': 'World!'}

@fixture
@mark.asyncio
async def fixture_post_form_url_encoded(fixture_api):
    async with fixture_api.session():
        return await fixture_api.method_post_form_url_encoded(
            body={'Hello': 'World!'}
        )

@mark.asyncio
async def test_post_form_url_encoded(fixture_post_form_url_encoded):
    response = fixture_post_form_url_encoded
    assert isinstance(response.get('form'), Dict)
    assert response.get('form') == {'Hello': 'World!'}

@mark.asyncio
async def test_concurrency(fixture_api):
    async with fixture_api.session():
        tasks = (
            fixture_api.method_get(),
            fixture_api.method_get_path_params(first_path='hello', second_path='world'),
            fixture_api.method_post_json(body={'Hello': 'World!'}),
            fixture_api.method_post_form_url_encoded(body={'Hello': 'World!'}),
        )
        responses = await gather(*tasks)
        assert isinstance(responses[0], Dict)
        assert responses[1].get('url') == 'http://httpbin.org/anything/hello/world'
        assert isinstance(responses[2].get('json'), Dict)
        assert responses[2].get('json') == {'Hello': 'World!'}
        assert isinstance(responses[3].get('form'), Dict)
        assert responses[3].get('form') == {'Hello': 'World!'}
