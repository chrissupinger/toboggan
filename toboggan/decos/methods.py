# Standard
from functools import wraps
from types import MappingProxyType
from typing import Dict, Text

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from ..builders import (
    StateBuilder as _StateBuilder,
    MessageBuilder as _MessageBuilder)
from ..models import MethodContext as _MethodContext

__all__ = ('Connect', 'Delete', 'Get', 'Head', 'Options', 'Patch', 'Post', 'Put', 'Trace',)


class _Context(_MethodContext, _StateBuilder, _MessageBuilder):
    """Constructor for the base context of an HTTP method.
    """

    def __init__(self, method: Text, path: Text, **kwargs: Dict):
        super().__init__(verb=method, path=path)

    def __call__(self, func):
        @wraps(func)
        def arg_handler(*args, **kwargs):
            self.path_params = kwargs
            self.set_method_from_args(annotations=func.__annotations__)
            session, settings, yields = self.get_state(
                mapping=MappingProxyType({obj.alias: obj for obj in args + (self,)}))
            if isinstance(session, Session):
                response = self.send_blocking_request(session, settings, yields)
            elif isinstance(session, ClientSession):
                response = self.send_nonblocking_request(session, settings, yields)
            return response
        return arg_handler


class Connect(_Context):
    """Constructor for a CONNECT HTTP method.\

    The CONNECT method establishes a tunnel to the server identified by the target resource.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Delete(_Context):
    """Constructor for a DELETE HTTP method.\

    The DELETE method deletes the specified resource.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Get(_Context):
    """Constructor for a GET HTTP method.\

    The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Head(_Context):
    """Constructor for a HEAD HTTP method.\

    The HEAD method asks for a response identical to a GET request, but without the response body.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Options(_Context):
    """Constructor for an OPTIONS HTTP method.\

    The OPTIONS method describes the communication options for the target resource.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Patch(_Context):
    """Constructor for a PATCH HTTP method.\

    The PATCH method applies partial modifications to a resource.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Post(_Context):
    """Constructor for a POST HTTP method.\

    The POST method submits an entity to the specified resource, often causing a change in state or side effects on the
    server.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Put(_Context):
    """Constructor for a PUT HTTP request.\

    The PUT method replaces all current representations of the target resource with the request payload.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)


class Trace(_Context):
    """Constructor for a TRACE HTTP method.\

    The TRACE method performs a message loop-back test along the path to the target resource.\

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """
    def __init__(self, path: Text = '') -> None:
        super().__init__(method=self.__class__.__name__.upper(), path=path)
