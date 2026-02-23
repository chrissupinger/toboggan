# Standard
from functools import wraps
from typing import Callable

# Local
from .contexts import _ctx_sends_type
from toboggan.aliases import AliasSendsType
from toboggan.connector import Connector
from toboggan.interfaces import InterfaceDecoContext

__all__ = ('sends',)


class Sends:
    __slots__ = ('form_url_encoded', 'json',)

    def __init__(self) -> None:
        self.form_url_encoded = self.Data()
        """Default to sending form-encoded data in the request

        ::
        
            @sends.form_url_encoded
            @post(path='/post')
            def post_data(self, body: Body): pass
        """
        self.json = self.Json()
        """Default to sending JSON data in the request.

        ::
        
            @sends.json
            @post(path='/post')
            def post_json(self, body: Body): pass
        """

    class _Context(InterfaceDecoContext):
        __slots__ = ('__context',)

        def __init__(self, context: AliasSendsType) -> None:
            self.__context: AliasSendsType = context

        def __call__(self, func: Callable, **kwargs) -> Callable:
            @wraps(func)
            def wrapper(*args: Connector, **kwargs) -> Callable:
                ctx_sends_type = _ctx_sends_type.set(self.__context)
                try:
                    return func(*args, **kwargs)
                finally:
                    _ctx_sends_type.reset(ctx_sends_type)
            return wrapper

    class Data(_Context):

        def __init__(self) -> None:
            super().__init__(context=AliasSendsType.DATA)

    class Json(_Context):

        def __init__(self) -> None:
            super().__init__(context=AliasSendsType.JSON)


sends = Sends()
"""Provides access to decorators that allow a method to default to sending
form-encoded data or JSON.  Declaring a subsequent send type will overwrite a
previous declared send type."""
