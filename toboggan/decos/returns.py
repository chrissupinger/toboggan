# Standard
from functools import wraps
from typing import Callable, List, Tuple, Union, Optional

# Local
from toboggan.aliases import AliasReturnType
from toboggan.connector import Connector
from toboggan.interfaces import InterfaceDecoCommon, InterfaceDecoContext
from toboggan.decos.contexts import _ctx_returns_type, _ctx_returns_json_value

__all__ = ('returns',)


class Returns(InterfaceDecoCommon):

    def __init__(self):
        self.json = self.Json()
        """If wanting to exclusively return the response's JSON object, a flat
        decoration can be used
        
        ::
        
            @returns.json
            @get(path='/get')
            def get_(self, **kwargs): pass
            
        Values can be passed to the `key` argument.  This is not required.  If
        used, the values passed will be attempted to be negotiated.  `key` can
        be of type `list`, `tuple`, `str` or `None`
        
        ::
        
            @returns.json(key=...)
            @get(path='/get')
            def get_(self, **kwargs): pass
        """
        self.status_code = self.StatusCode()
        """The response's status code can be exclusively returned

        ::
        
            @returns.status_code
            @post(path='/post')
            def post_(self, **kwargs): pass
        """
        self.text = self.Text()
        """The response's text representation can be exclusively returned

        ::
        
            @returns.text
            @delete(path='/delete')
            def delete_(self, **kwargs): pass
        """

    class _Context(InterfaceDecoContext):
        __slots__ = ('__context', '__key')

        def __init__(self, context, **kwargs):
            self.__context = context
            self.__key = kwargs.get('key')

        def __call__(self, func, **kwargs):

            @wraps(func)
            def wrapper(*args: Connector, **kwargs):
                ctx_returns_type = _ctx_returns_type.set(self.__context)
                ctx_return_json_value = _ctx_returns_json_value.set(self.__key)
                try:
                    return func(*args, **kwargs)
                finally:
                    _ctx_returns_type.reset(ctx_returns_type)
                    if self.__context is AliasReturnType.JSON and self.__key:
                        _ctx_returns_json_value.reset(ctx_return_json_value)
            return wrapper

    class Json(_Context):

        def __init__(
                self, key: Optional[Union[str, List[str], Tuple[str]]] = None
        ) -> None:
            super().__init__(context=AliasReturnType.JSON, key=key)

        def __call__(
                self, func: Optional[Callable] = None, **kwargs
        ) -> Callable:
            if not func:
                return self.__class__(**kwargs)
            return super().__call__(func=func)

    class StatusCode(_Context):

        def __init__(self) -> None:
            super().__init__(context=AliasReturnType.STATUS_CODE)

    class Text(_Context):

        def __init__(self) -> None:
            super().__init__(context=AliasReturnType.TEXT)


returns = Returns()
"""Provides access to decorators that allow a method to default to returning
JSON, text or status code when invoked.  Declaring a subsequent return type
will overwrite a previous declared return type."""
