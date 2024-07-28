# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Table of contents

- [Connector](#connector)
- [Client](#client)
- [Decorators](#decorators)
  - [Verbs](#verbs)
  - [headers](#headers)
  - [params](#params)
  - [returns.*](#returns)
- [Annotations](#annotations)
  - [Body](#body)
  - [Path](#path)
  - [Query](#query)
  - [QueryMap](#querymap)
- [Examples](#examples)
  - [Blocking](#blocking-w-httpbin)
  - [Nonblocking](#nonblocking-w-pokéapi)

### Connector

The `Connector` class is the base configuration for creating all API models.  It can grant any instance method access
to a common client session and a wide array of settings.  Instantiation can be achieved in various ways:

- Initialization of the inherited superclass in the class's constructor

``` python
from toboggan import Connector


class Httpbin(Connector):

    def __init__(self):
        super().__init__(base_url='https://httpbin.org')


httpbin = Httpbin()
```

- Directly calling the class constructor with arguments

``` python
from toboggan import Connector


class Httpbin(Connector):
    pass


httpbin = Httpbin(base_url='https://httpbin.org')
```

The `Connector` class is built for reusability.  Even after initial instantiation, the `Connector` can be
re-instantiated with new `base_url` and `client` arguments.  A use case for this is reusing a model in which both
blocking and nonblocking behavior is desired from mutual or exclusive paths.

``` python
from toboggan import AiohttpClient, Path, RequestsClient, get, headers


@headers({'Content-Type': 'application/json'})
class PokeApi(Connector):

    @get(path='/pokemon/{no}')
    def pokemon(self, no: Path) -> Dict:
        pass


pokeapi_blocking = PokeApi(base_url='https://pokeapi.co/api/v2', client=RequestClient())
pokeapi_nonblocking = pokeapi_blocking(base_url='https://pokeapi.co/api/v2', client=AiohttpClient())
```

### Client

The default client associated to the `Connector` class is the native `RequestsClient`.  For nonblocking requests, the
native `AiohttpClient` can be used.  `aiohttp.ClientSession` and `requests.Session` are compatible as client types.
Changing the client type can be achieved through:

- Passing `AiohttpClient` as a constructor argument

``` python
from toboggan import AiohttpClient

httpbin = Httpbin(base_url='https://httpbin.org', client=AiohttpClient())
```

- Setting the client via the `session` setter

``` python
from toboggan import RequestsClient

httpbin.session = RequestsClient()
```

### Decorators

#### Verbs

The verb decorators are foundational for your instance methods to use the `Connector` and should be applied as the first
decorator in a chain.  A verb decorator is the minimum requirement for instance methods using the `Connector`.

The following HTTP verbs are available for use:
- `connect`
- `delete`
- `get`
- `head`
- `options`
- `patch`
- `post`
- `put`
- `trace`

``` python
from toboggan import Connector, get, post


class Httpbin(Connector):
    
    @get(path='/get')
    def get_(self):
        pass


httpbin = Httpbin(base_url='https://httpbin.org')
```

#### headers

The `headers` decorator is versatile and can be employed at both the class-level and its instance methods.  When
decorating the subclass of the `Connector` class, `headers` will designate global values to be applied to every instance
method that uses the `Connector`.  When decorating an instance method, those values are exclusive to the method.

``` python
@headers({'Content-Type': 'application/json'})
class Httpbin(Connector):

    @headers({'User-Agent': 'toboggan (python-requests/2.32.3)'})
    @get(path='/get')
    def get_(self):
        pass
```

#### params

#### returns.*

### Annotations

#### Body

...

#### Path

...

#### Query

...

#### QueryMap

...

### Examples

#### Blocking w/ [httpbin](https://github.com/postmanlabs/httpbin)

``` python
from json import dumps
from toboggan import Body, Connector, ResponseObject, get, headers, post


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

    @get(path='/get')
    def get_(self) -> ResponseObject:
        """The request's query parameters.
        """

    @post(path='/post')
    def post_(self, body: Body) -> ResponseObject:
        """The request's POST parameters.
        """


if __name__ == '__main__':
    httpbin = Httpbin(base_url='http://0.0.0.0')

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

#### Nonblocking w/ [PokéAPI](https://pokeapi.co/)

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
