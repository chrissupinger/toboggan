# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's initial support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Blocking usage w/ [httpbin](https://github.com/postmanlabs/httpbin)

### Model

``` python
from toboggan import Connector, Body, Get, Headers


@Headers({'Content-Type': 'application/json'})
class Httpbin(Connector):
    """Represents an httpbin API mapping.
    """

    def __init__(self):
        super().__init__(base_url='https://httpbin.org')

    @Get(path='ip')
    def get_ip(self):
        """Retrieve remote IP address.
        """

    @Post(path='/post')
    def send_body(self, body: Body):
        """Send a post request.
        """

```

### Instantiation

``` python
httpbin = Httpbin()

```

### Invocations

``` python
my_ip = httpbin.get_ip()
my_post = httpbin.send_body(body={'hello': 'world'})

```

### Responses

``` python
print(my_ip.status_code)
# 200
print(my_ip.json())
# {'origin': '<YOUR_IP_ADDRESS>'}
print(my_post.status_code)
# 200
print(my_post.json())
# {'args': {}, 'data': '{"hello": "world"}', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Length': '18', 'Content-Type': 'application/json', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.28.2'}, 'json': {'hello': 'world'}, 'origin': '<YOUR_IP_ADDRESS>', 'url': 'https://httpbin.org/post'}

```

## Nonblocking usage w/ [PokéAPI](https://pokeapi.co/)

### Model

``` python
import asyncio
from toboggan import Client, Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class PokeApi(Connector):
    """Represents a PokéAPI mapping.
    """

    @Get(path='pokemon/{no}')
    def get_pokemon(self, no):
        """Retrieve Pokémon metadata.
        """

```

### Methods

``` python
async def get_pokemon(session, request):
    async with session.request(**request) as response:
        return await response.json()

async def get_all_pokemon(range_):
    api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.client.session(**api.client.settings) as session:
        futures = [asyncio.ensure_future(get_pokemon(session, request)) for request in pokemon]
        responses = await asyncio.gather(*futures)
        return responses

```

### Invocation

``` python
responses = asyncio.run(get_all_pokemon(range_=range(1, 152)))

```

### Responses

``` python
print(responses)
# [{'abilities': [{'ability': {'name': 'overgrow', 'url': 'https://pokeapi.co/api/v2/ability/65/'}, 'is_hidden': False, 'slot': 1}, {'ability': {'name': 'chlorophyll', 'url': 'https://pokeapi.co/api/v2/ability/34/'}, 'is_hidden': True, 'slot': 3}], 'base_experience': 64, 'forms': [{'name': 'bulbasaur', ...}]

```
