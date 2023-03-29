# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's initial support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Blocking usage w/ [httpbin](https://github.com/postmanlabs/httpbin)

### Model

``` python
from toboggan import Body, Client, Connector, Get, Headers, Post, QueryParam


@Headers({'Content-Type': 'application/json'})
class Httpbin(Connector):
    """Represents an httpbin API mapping.
    """

    def __init__(self):
        super().__init__(base_url='https://httpbin.org', client=Client.block())

    @Get(path='/ip')
    def get_ip(self):
        """Send a GET request retrieve your remote IP address.
        """

    @Get(path='/get')
    def get_w_query_params(self, hello: QueryParam):
        """Send a GET request w/ query parameters.
        """

    @Post(path='/post')
    def post_w_body(self, body: Body):
        """Send a POST request w/ body.
        """

```

### Instantiation

``` python
httpbin = Httpbin()

```

### Invocations

``` python
get_ip = httpbin.get_ip()
get_w_query_params = httpbin.get_w_query_params(hello='world')
post_w_body = httpbin.post_w_body(body={'hello': 'world'})

```

### Responses

``` python
print(get_ip.status_code)
200

print(get_ip.json())
{
    'origin': '<YOUR_IP_ADDRESS>'
}

print(get_w_query_params.json())
{
    'args': {
        'hello': 'world'
    },
    'headers': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Host': 'httpbin.org',
        'User-Agent': 'python-requests/2.28.2'
    },
    'origin': '<YOUR_IP_ADDRESS>',
    'url': 'https://httpbin.org/get?hello=world'
}

print(post_w_body.json())
{
    'args': {},
    'data': '{"hello": "world"}',
    'files': {},
    'form': {},
    'headers': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Length': '18',
        'Content-Type': 'application/json',
        'Host': 'httpbin.org',
        'User-Agent': 'python-requests/2.28.2'
    },
    'json': {
        'hello': 'world'
    },
    'origin': '<YOUR_IP_ADDRESS>',
    'url': 'https://httpbin.org/post'
}

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

    @Get(path='/pokemon/{no}')
    def get_pokemon(self, no):
        """Retrieve Pokémon metadata.
        """

```

### Invocations

#### 1.  Request

``` python
async def fetch(session, request):
    async with session.request(**request) as response:
    json_ = await response.json()
    return json_['species']['name']

```

#### 2.  Requests handler

##### Example A. Using asyncio.run; Python 3.7 and above

``` python
async def get_all_pokemon(range_):
    api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.session(**api.settings) as session:
        responses = await asyncio.gather(*[fetch(session, request) for request in pokemon])
        return responses

```

##### Example B. Using an event loop; Python 3.6 and below

``` python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())

async def get_all_pokemon(range_):
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.session(**api.settings) as session:
        responses = await asyncio.gather(*[fetch(session, request) for request in pokemon])
        return responses

results = loop.run_until_complete(get_all_pokemon(range_=range(1, 152)))

```

##### Example C. Using futures and asyncio.run

``` python
async def get_all_pokemon(range_):
    api = PokeApi(base_url='https://pokeapi.co/api/v2', client=Client.nonblock())
    pokemon = [api.get_pokemon(no=no) for no in range_]
    async with api.session(**api.settings) as session:
        futures = [asyncio.ensure_future(fetch(session, request)) for request in pokemon]
        responses = await asyncio.gather(*futures)
        return responses

results = asyncio.run(get_all_pokemon(range_=range(1, 152)))

```

### Responses

``` python
print(results)
['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard',
'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle',
'kakuna', 'beedrill', 'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate',
'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu', 'sandshrew', 'sandslash',
'nidoran-f', 'nidorina', 'nidoqueen', 'nidoran-m', 'nidorino', 'nidoking', 'clefairy',
'clefable', 'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat',
'oddish', 'gloom', 'vileplume', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett',
'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe',
'arcanine', 'poliwag', 'poliwhirl', 'poliwrath', 'abra', 'kadabra', 'alakazam',
'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool',
'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash', 'slowpoke',
'slowbro', 'magnemite', 'magneton', 'farfetchd', 'doduo', 'dodrio', 'seel', 'dewgong',
'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix',
'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'electrode', 'exeggcute', 'exeggutor',
'cubone', 'marowak', 'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing',
'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan', 'horsea', 'seadra', 'goldeen',
'seaking', 'staryu', 'starmie', 'mr-mime', 'scyther', 'jynx', 'electabuzz', 'magmar',
'pinsir', 'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee', 'vaporeon',
'jolteon', 'flareon', 'porygon', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl',
'snorlax', 'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair', 'dragonite',
'mewtwo', 'mew']

```
