# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's initial support for nonblocking requests with [AIOHTTP](https://github.com/aio-libs/aiohttp).

## Blocking usage w/ [httpbin](https://github.com/postmanlabs/httpbin)

### Your class

``` python
from toboggan import Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class Httpbin(Connector):

	def __init__(self):
		super().__init__(base='https://httpbin.org')

	@Get(path='ip')
	def get_ip(self):
		"""Retrieves your remote IP address.
		"""

```

### Your instantiation

``` python
httpbin = Httpbin()

```

### Your invocation

``` python
my_ip = httpbin.get_ip()

```

### Your response

``` python
print(my_ip.status_code)
# 200
print(my_ip.json)
# {'origin': '<YOUR_IP_ADDRESS>'}

```

## Nonblocking usage w/ [PokéAPI](https://pokeapi.co/)

### Your classes and instantiations

``` python
import asyncio
from toboggan import Client, Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class PokeApi(Connector):

	@Get(path='pokemon/{no}')
	def get_pokemon(self, no):
		"""Retrieves Pokémon metadata.
		"""

		
class PokeApiAsync:

    def __init__(self):
        self.futures = list()

    @staticmethod
    async def get_pokemon(session, request):
        async with session.request(**request) as response:
            return await response.json()

    async def get_gen_one(self, range_):
        poke_api = PokeApi(base='https://pokeapi.co/api/v2', client=Client.nonblock())
        gen_one = [poke_api.get_pokemon(no=no) for no in range_]
        async with poke_api.client.session(**poke_api.client.settings) as session:
            for request in gen_one:
                self.futures.append(asyncio.ensure_future(self.get_pokemon(session, request)))
            responses = await asyncio.gather(*self.futures)
            return responses

poke_api_async = PokeApiAsync()
asyncio.run(poke_api_async.get_gen_one(range_=range(1, 152))

```
