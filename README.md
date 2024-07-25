# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Example usage

### Blocking w/ [httpbin](https://github.com/postmanlabs/httpbin)

``` python
from json import dumps
from toboggan import (
    Body, Connector, RequestsClient, ResponseObject, get, headers, post,)


@headers({'Content-Type': 'application/json'})
class Httpbin(Connector):
    """A httpbin mapping.

    This example and mapping is facilitated with the Docker image.  To run it
    locally, see usage below.

    If wanting to use the hosted httpbin service, set the `base_url` to
    https://httpbin.org.

    ::

        docker pull kennethreitz/httpbin
        docker run -p 80:80 kennethreitz/httpbin

    References:
        - `httpbin hosted <https://httpbin.org/>`_
        - `httpbin on GitHub <https://github.com/postmanlabs/httpbin>`_
    """

    def __init__(self):
        super().__init__(base_url='http://0.0.0.0', client=RequestsClient())

    @get(path='/get')
    def get_(self) -> ResponseObject:
        """The request's query parameters.
        """

    @post(path='/post')
    def post_(self, body: Body) -> ResponseObject:
        """The request's POST parameters.
        """


if __name__ == '__main__':
    httpbin = Httpbin()

    response = httpbin.get_()
    print(dumps(response.json(), indent=4, default=str))

    request_body = {
        "user_id": 12345,
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "Hello, world!",
        "tags": ["general", "greeting"],
        "data": {
            "age": 30,
            "city": "New York"
        }
    }
    response = httpbin.post_(body=request_body)
    print(dumps(response.json(), indent=4, default=str))

```

### Nonblocking w/ [PokéAPI](https://pokeapi.co/)

``` python
import asyncio
from typing import Dict
from toboggan import AiohttpClient, Connector, Path, get, headers, returns


@headers({'Content-Type': 'application/json'})
class PokeApi(Connector):
    """A PokéAPI mapping.

    References:
        - `PokéAPI <https://pokeapi.co>`_
    """

    def __init__(self):
        super().__init__(
            base_url='https://pokeapi.co/api/v2', client=AiohttpClient())

    @returns.json(key=('species', 'name',))
    @get(path='/pokemon/{no}')
    def pokemon(self, no: Path) -> Dict:
        """Retrieve Pokémon metadata.  Traverse the nested dictionary returned
        and get the `name` value.

        References:
            - `Pokémon (endpoint) <https://pokeapi.co/docs/v2#pokemon>`_
        """


if __name__ == '__main__':
    # Utilizing `asyncio.run` for Python 3.7 and above.
    async def get_pokemon(no):
        api = PokeApi()
        async with api.session:
            return await api.pokemon(no=no)

    response = asyncio.run(get_pokemon(no=1))
    print(response)

    async def get_many_pokemon(range_):
        api = PokeApi()
        async with api.session:
            tasks = await asyncio.gather(
                *[api.pokemon(no=no) for no in range_])
            return tasks

    responses = asyncio.run(get_many_pokemon(range_=range(1, 152)))
    print(responses)

    # For < 3.7, use an event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(get_many_pokemon(range_=range(1, 152)))
    print(responses)

```
