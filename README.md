# toboggan

Most def inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's initial support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Blocking usage w/ [httpbin](https://github.com/postmanlabs/httpbin)

### Your class

``` python
from toboggan import Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class Httpbin(Connector):

	def __init__(self):

		super().__init__(base='https://httpbin.org')

	@Get(path='ip')
	def ip(self):
		"""Retrieves your remote IP address.
		"""
```

### Your instantiation

``` python
httpbin = Httpbin()
```

### Your invocation

``` python
myIp = httpbin.ip()
```

### Your response

``` python
print(myIp.status_code)
# 200

print(myIp.json)
# {'origin': '<YOUR_IP_ADDRESS>'}
```

## Nonblocking usage w/ [PokéAPI](https://pokeapi.co/)

### Your class

``` python
from toboggan import ClientType, Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class PokeApi(Connector):

	@Get(path='api/v2/pokemon/{no}')
	def pokemon(self):
		"""Retrieves Pokémon metadata.
		"""
```

### Your instantiation

``` python
pokeapi = PokeApi(base='https://pokeapi.co', client=ClientType.nonblock)
```

### Your pool

``` python
requests = [pokeapi.pokemon(no=no) for no in range(1, 151)]
```

### Your invocation

``` python
pokeapi.staging.send(requests)
```

### Retrieving your responses

``` python
for resp in pokeapi.staging.responses:

	print(resp.status_code)
	# 200

	print(resp.json)
	# {'abilities': [{'ability': {'name': ...}, ...]}
```