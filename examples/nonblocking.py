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
