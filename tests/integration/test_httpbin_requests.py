# Standard
from typing import Dict

# Third-party
from pytest import fixture

# Local
from toboggan import Body, Connector, Path, get, post, sends


class HttpBin(Connector):

    def __init__(self, base_url: str = 'http://httpbin.org/') -> None:
        super().__init__(base_url=base_url)

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
def fixture_api():
    return HttpBin()

@fixture
def fixture_get(fixture_api):
    return fixture_api.method_get()

def test_get_json(fixture_get):
    assert isinstance(fixture_get.json(), Dict)

def test_get_status_code(fixture_get):
    assert isinstance(fixture_get.status_code, int)

def test_get_text(fixture_get):
    assert isinstance(fixture_get.text, str)

@fixture
def fixture_get_path_params(fixture_api):
    return fixture_api.method_get_path_params(
        first_path='hello', second_path='world'
    )

def test_get_path_params(fixture_get_path_params):
    response = fixture_get_path_params.json()
    assert response.get('url') == 'http://httpbin.org/anything/hello/world'

@fixture
def fixture_post_json(fixture_api):
    return fixture_api.method_post_json(body={'Hello': 'World!'})

def test_post_json(fixture_post_json):
    response = fixture_post_json.json()
    assert isinstance(response.get('json'), Dict)
    assert response.get('json') == {'Hello': 'World!'}

@fixture
def fixture_post_form_url_encoded(fixture_api):
    return fixture_api.method_post_form_url_encoded(
        body={'Hello': 'World!'}
    )

def test_post_form_url_encoded(fixture_post_form_url_encoded):
    response = fixture_post_form_url_encoded.json()
    assert isinstance(response.get('form'), Dict)
    assert response.get('form') == {'Hello': 'World!'}
