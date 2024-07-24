# Standard
from typing import Any, Dict, NewType, Union

__all__ = ('Body', 'Path', 'Query', 'QueryMap',)

Body = NewType('Body', Union[Dict, str])
"""Annotates a parameter that will bind the body.

Usage::

    @post(path='/post')
    def post_(self, body: Body): pass
"""
Path = NewType('Path', Union[str, Any])
"""Annotates a parameter that will bind path parameters.

Usage::

    @get(path='/get/{first_path_param}/{second_path_param})
    def get_(self, first_path_param: Path, second_path_param: Path): pass
"""
Query = NewType('Query', Union[int, str])
"""Annotates a parameter that will bind a query parameter.

Usage::

    @get(path='/get')
    def get_(self, first_query: Query, second_query: Query): pass
"""
QueryMap = NewType('QueryMap', Union[int, str])
"""Annotates a parameter that will bind query parameters.

Usage::

    @get(path='/get')
    def get_(self, **mapping_of_queries: QueryMap): pass
"""
