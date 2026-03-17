# Standard
from typing import Dict

# Third-party
from pytest import fixture, raises
from pydantic import BaseModel, HttpUrl

# Local
from toboggan import Connector, Path, get, returns


class ValidModelGetHttpbin(BaseModel):
    args: Dict
    headers: Dict
    origin: str
    url: HttpUrl


class InvalidModelGetHttpbin(BaseModel):
    args: int
    headers: int
    origin: int
    url: int


class HttpBin(Connector):

    def __init__(self, base_url: str = 'http://httpbin.org/') -> None:
        super().__init__(base_url=base_url)

    @returns.json
    @get(path='anything')
    def method_get(self) -> ValidModelGetHttpbin:
        pass

    @returns.json
    @get(path='anything/{first_path}/{second_path}')
    def method_get_path_params(
        self, first_path: Path, second_path: Path
    ) -> InvalidModelGetHttpbin:
        pass


@fixture
def fixture_api():
    return HttpBin()

def test_valid_return(fixture_api):
    response = fixture_api.method_get()
    assert isinstance(response.args, Dict)
    assert isinstance(response.headers, Dict)
    assert isinstance(response.origin, str)
    assert response.url == HttpUrl('http://httpbin.org/anything')

def test_invalid_return(fixture_api):
    with raises(Exception):
        fixture_api.method_get_path_params(
            first_path='hello', second_path='world'
        )
