# Standard
from enum import Enum

__all__ = ('Client', 'Header', 'Request', 'Response', 'Scheme', 'Verb',)


class Client(str, Enum):
    blocking = 'blocking'
    nonblocking = 'nonblocking'
    session = 'session'


class Header(str, Enum):
    user_agent = 'User-Agent'


class Request(str, Enum):
    cookies = 'cookies'
    data = 'data'
    headers = 'headers'
    json = 'json'
    params = 'params'
    method = 'method'
    url = 'url'


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
