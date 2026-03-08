# Standard
from typing import Dict, NewType

__all__ = ('Body', 'Options', 'Path', 'Query', 'QueryKebab',)

Body = NewType(name='Body', tp=Dict)
"""Annotates a parameter that will bind the body

::

    @post(path='/post')
    def post_request(self, body: Body): pass
"""
Options = NewType(name='Options', tp=Dict)
"""Annotates a parameter that will bind options for the request.

This is specific to the underlying client implementation.
- For `Requests`: [requests.Session.request](https://docs.python-requests.org/en/latest/api/#requests.Session.request)
- For `aiohttp`: [aiohttp.ClientSession.request](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request)
- For `httpx`: [httpx.request](https://www.python-httpx.org/api/)

::

    @get(path='/get')
    def get_w_options(self, options: Options): pass
"""
Path = NewType(name='Path', tp=str)
"""Annotates a parameter that will bind path parameters

::

    @get(path='/get/{first}/{second})
    def get_w_path_params(self, first: Path, second: Path): pass
"""
Query = NewType(name='Query', tp=str)
"""Annotates a parameter that will bind a query parameter

::

    @get(path='/get')
    def get_w_query_params(self, first: Query, second: Query): pass
"""
QueryKebab = NewType(name='QueryKebab', tp=str)
"""Annotates a parameter that will bind a query parameter and implement kebab 
case for keys.  This requires that a the query parameter key be delimited by an 
underscore.

e.g., `{'kebab_query': 'value'} == {'kebab-query': 'value'}`

::

    @get(path='/get')
    def get_w_query_params(self, first: Query, kebab_query: QueryKebab): pass
"""
