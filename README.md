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

### Invocations

#### 1.  Request

``` python
import asyncio


async def fetch(session, request):
    async with session.request(**request) as response:
    json_ = await response.json()
    return json_['species']['name']

```

#### 2.  Requests handler

##### Example A. Using an event loop

``` python
async def get_all_pokemon(range_):
    api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.client.session(**api.client.settings) as session:
        responses = await asyncio.gather(*[fetch(session, request) for request in pokemon])
        return responses

loop = asyncio.get_event_loop()
results = loop.run_until_complete(get_all_pokemon(range_=range(1, 152)))

```

##### Example B. Using futures

``` python
async def get_all_pokemon(range_):
    api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.client.session(**api.client.settings) as session:
        futures = [asyncio.ensure_future(fetch(session, request)) for request in pokemon]
        responses = await asyncio.gather(*futures)
        return responses

results = asyncio.run(get_all_pokemon(range_=range(1, 152)))

```

### Responses

``` python
print(results)
# ['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate', 'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu', 'sandshrew', 'sandslash', 'nidoran-f', 'nidorina', 'nidoqueen', 'nidoran-m', 'nidorino', 'nidoking', 'clefairy', 'clefable', 'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'oddish', 'gloom', 'vileplume', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath', 'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool', 'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash', 'slowpoke', 'slowbro', 'magnemite', 'magneton', 'farfetchd', 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'electrode', 'exeggcute', 'exeggutor', 'cubone', 'marowak', 'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing', 'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan', 'horsea', 'seadra', 'goldeen', 'seaking', 'staryu', 'starmie', 'mr-mime', 'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir', 'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee', 'vaporeon', 'jolteon', 'flareon', 'porygon', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'snorlax', 'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair', 'dragonite', 'mewtwo', 'mew']

```
