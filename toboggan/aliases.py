# Standard
from enum import Enum

__all__ = (
    'Annotation',
    'Client',
    'Header',
    'Request',
    'Response',
    'Scheme',
    'Send',
    'Verb',
)


class Annotation(str, Enum):
    body = 'Body'
    path = 'Path'
    query = 'Query'
    query_kebab = 'QueryKebab'
    query_map = 'QueryMap'
    query_map_kebab = 'QueryMapKebab'


class Client(str, Enum):
    blocking = 'blocking'
    nonblocking = 'nonblocking'
    session = 'session'


class Header(str, Enum):
    user_agent = 'User-Agent'


class Request(str, Enum):
    allow_redirects = 'allow_redirects'
    cert = 'cert'
    cookies = 'cookies'
    data = 'data'
    headers = 'headers'
    json = 'json'
    method = 'method'
    params = 'params'
    send_format = 'send_format'
    ssl = 'ssl'
    timeout = 'timeout'
    url = 'url'
    verify = 'verify'


class Response(str, Enum):
    json = 'json'
    returns = 'returns'
    status_code = 'status_code'
    text = 'text'


class Scheme(str, Enum):
    data = 'data'
    ftp = 'ftp'
    file = 'file'
    http = 'http'
    https = 'https'
    irc = 'irc'
    mailto = 'mailto'


class Send(str, Enum):
    data = 'data'
    json = 'json'


class Verb(str, Enum):
    connect = 'CONNECT'
    delete = 'DELETE'
    get = 'GET'
    head = 'HEAD'
    options = 'OPTIONS'
    patch = 'PATCH'
    post = 'POST'
    put = 'PUT'
    trace = 'TRACE'
