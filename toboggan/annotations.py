# Standard
from typing import NewType, Union

# Local
from .aliases import Annotation

__all__ = 'Body', 'Path', 'Query', 'QueryKebab', 'QueryMap', 'QueryMapKebab'

Body = NewType(name=Annotation.body, tp=Union[dict, str])
"""Annotates a parameter that will bind the body.

Usage::

    @post(path='/post')
    def post_(self, body: Body): pass
"""
Path = NewType(name=Annotation.path, tp=Union[str, int])
"""Annotates a parameter that will bind path parameters.

Usage::

    @get(path='/get/{first_path_param}/{second_path_param})
    def get_(self, first_path_param: Path, second_path_param: Path): pass
"""
Query = NewType(name=Annotation.query, tp=Union[str, str])
"""Annotates a parameter that will bind a query parameter.

Usage::

    @get(path='/get')
    def get_(self, first_query: Query, second_query: Query): pass
"""
QueryKebab = NewType(name=Annotation.query_kebab, tp=Union[str, str])
"""Annotates a parameter that will bind a query parameter and implement kebab 
case for keys.  This requires that a the query parameter key be delimited by an 
underscore.

e.g., `{'first_query': 'value'} == {'first-query': 'value'}`

Usage::

    @get(path='/get')
    def get_(self, first_query: QueryKebab, second_query: QueryKebab): pass
"""
QueryMap = NewType(name=Annotation.query_map, tp=Union[str, str])
"""Annotates a parameter that will bind query parameters.

Usage::

    @get(path='/get')
    def get_(self, **mapping_of_queries: QueryMap): pass
"""
QueryMapKebab = NewType(name=Annotation.query_map_kebab, tp=Union[str, str])
"""Annotates a parameter that will bind query parameters and implement kebab 
case for keys.  This requires that a the query parameter keys be delimited by 
underscores.

e.g., `{'first_query': 'value', 'second_query': 'value'} == {'first-query': 'value', 'second-query': 'value'}`

Usage::

    @get(path='/get')
    def get_(self, **mapping_of_queries: QueryMapKebab): pass
"""
