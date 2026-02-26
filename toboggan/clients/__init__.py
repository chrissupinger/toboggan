# Local
from .requests_ import requests_
from .resolvers import ResolverRequest, resolve_client_type
try:
    from .aiohttp_ import aiohttp_
except ModuleNotFoundError:
    aiohttp_ = None
