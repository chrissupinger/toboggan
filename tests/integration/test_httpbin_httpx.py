# Standard
from asyncio import gather
from typing import Dict

# Third-party
from pytest import fixture, mark
from httpx import AsyncClient, Client

# Local
from toboggan import Body, Connector, Path, get, post, sends


class HttpBin(Connector):

    def __init__(
            self, base_url: str = 'http://httpbin.org/', client=Client()
        ) -> None:
        super().__init__(base_url=base_url, client=client)

    @get(path='anything')
    def method_get(self):
        pass

    @get(path='anything/{first_path}/{second_path}')
    def method_get_path_params(self, first_path: Path, second_path: Path):
        pass
    
    @sends.json
    @post(path='anything')
    def method_post_json(self, body: Body):
        pass
    
    @sends.form_url_encoded
    @post(path='anything')
    def method_post_form_url_encoded(self, body: Body):
        pass


@fixture
def fixture_api_sync():
    return HttpBin()

@fixture
def fixture_get_sync(fixture_api_sync):
    return fixture_api_sync.method_get()

def test_get_json_sync(fixture_get_sync):
    assert isinstance(fixture_get_sync.json(), Dict)

def test_get_status_code_sync(fixture_get_sync):
    assert isinstance(fixture_get_sync.status_code, int)

def test_get_text_sync(fixture_get_sync):
    assert isinstance(fixture_get_sync.text, str)

@fixture
def fixture_get_path_params_sync(fixture_api_sync):
    return fixture_api_sync.method_get_path_params(
        first_path='hello', second_path='world'
    )

def test_get_path_params_sync(fixture_get_path_params_sync):
    response = fixture_get_path_params_sync.json()
    assert response.get('url') == 'http://httpbin.org/anything/hello/world'

@fixture
def fixture_post_json_sync(fixture_api_sync):
    return fixture_api_sync.method_post_json(body={'Hello': 'World!'})

def test_post_json_sync(fixture_post_json_sync):
    response = fixture_post_json_sync.json()
    assert isinstance(response.get('json'), Dict)
    assert response.get('json') == {'Hello': 'World!'}

@fixture
def fixture_post_form_url_encoded_sync(fixture_api_sync):
    return fixture_api_sync.method_post_form_url_encoded(
        body={'Hello': 'World!'}
    )

def test_post_form_url_encoded_sync(fixture_post_form_url_encoded_sync):
    response = fixture_post_form_url_encoded_sync.json()
    assert isinstance(response.get('form'), Dict)
    assert response.get('form') == {'Hello': 'World!'}

@fixture
@mark.asyncio
async def fixture_api_async():
    httpbin = HttpBin()
    return httpbin(client=AsyncClient())

@fixture
@mark.asyncio
async def fixture_get_async(fixture_api_async):
    async with fixture_api_async.session():
        return await fixture_api_async.method_get()

@mark.asyncio
async def test_get_json_async(fixture_get_async):
    assert isinstance(fixture_get_async.json(), Dict)

@fixture
@mark.asyncio
async def fixture_get_path_params_async(fixture_api_async):
    async with fixture_api_async.session():
        return await fixture_api_async.method_get_path_params(
            first_path='hello', second_path='world'
        )

@mark.asyncio
async def test_get_path_params_async(fixture_get_path_params_async):
    response = fixture_get_path_params_async.json()
    assert response.get('url') == 'http://httpbin.org/anything/hello/world'

@fixture
@mark.asyncio
async def fixture_post_json_async(fixture_api_async):
    async with fixture_api_async.session():
        return await fixture_api_async.method_post_json(body={'Hello': 'World!'})

@mark.asyncio
async def test_post_json_async(fixture_post_json_async):
    response = fixture_post_json_async.json()
    assert isinstance(response.get('json'), Dict)
    assert response.get('json') == {'Hello': 'World!'}

@fixture
@mark.asyncio
async def fixture_post_form_url_encoded_async(fixture_api_async):
    async with fixture_api_async.session():
        return await fixture_api_async.method_post_form_url_encoded(
            body={'Hello': 'World!'}
        )

@mark.asyncio
async def test_post_form_url_encoded_async(fixture_post_form_url_encoded_async):
    response = fixture_post_form_url_encoded_async.json()
    assert isinstance(response.get('form'), Dict)
    assert response.get('form') == {'Hello': 'World!'}

@mark.asyncio
async def test_concurrency_async(fixture_api_async):
    async with fixture_api_async.session():
        tasks = (
            fixture_api_async.method_get(),
            fixture_api_async.method_get_path_params(first_path='hello', second_path='world'),
            fixture_api_async.method_post_json(body={'Hello': 'World!'}),
            fixture_api_async.method_post_form_url_encoded(body={'Hello': 'World!'}),
        )
        responses = await gather(*tasks)
        assert isinstance(responses[0].json(), Dict)
        assert responses[1].json().get('url') == 'http://httpbin.org/anything/hello/world'
        assert isinstance(responses[2].json().get('json'), Dict)
        assert responses[2].json().get('json') == {'Hello': 'World!'}
        assert isinstance(responses[3].json().get('form'), Dict)
        assert responses[3].json().get('form') == {'Hello': 'World!'}
