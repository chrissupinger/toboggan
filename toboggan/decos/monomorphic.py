# Standard
from functools import wraps
from typing import Callable, Optional, Union

# Local
from .contexts import (
    _ctx_returns_type, _ctx_returns_json_value, _ctx_sends_type,
)
from toboggan.aliases import AliasReturnType, AliasSendsType
from toboggan.connector import Connector


class _Context:
    __slots__ = ('__context', '__key',)

    def __init__(
            self, context: Union[AliasReturnType, AliasSendsType], **kwargs
    ) -> None:
        self.__context = context
        self.__key = kwargs.get('key')

    def __call__(self, func: Callable, **kwargs) -> Callable:

        @wraps(func)
        def wrapper(*args: Connector, **kwargs):
            if self.__context in (
                    AliasReturnType.JSON,
                    AliasReturnType.STATUS_CODE,
                    AliasReturnType.TEXT,
            ):
                return self._wrapper_returns(func, *args, **kwargs)
            elif self.__context in (AliasSendsType.DATA, AliasSendsType.JSON,):
                return self._wrapper_sends(func, *args, **kwargs)
        return wrapper

    def _wrapper_returns(self, func: Callable, *args: Connector, **kwargs):
        ctx_returns_type = _ctx_returns_type.set(self.__context)
        ctx_return_json_value = _ctx_returns_json_value.set(self.__key)
        try:
            return func(*args, **kwargs)
        finally:
            _ctx_returns_type.reset(ctx_returns_type)
            if self.__context is AliasReturnType.JSON and self.__key:
                _ctx_returns_json_value.reset(ctx_return_json_value)

    def _wrapper_sends(self, func: Callable, *args: Connector, **kwargs):
        ctx_sends_type = _ctx_sends_type.set(self.__context)
        try:
            return func(*args, **kwargs)
        finally:
            _ctx_sends_type.reset(ctx_sends_type)


class Returns:
    __slots__ = ('json', 'status_code', 'text',)

    def __init__(self):
        self.json = self.Json()
        """If wanting to exclusively return the response's JSON object, 
        a flat decoration can be used
        
        ::
        
            @returns.json
            @get(path='/get')
            def get_(self, **kwargs): pass
            
        Values can be passed to the `key` argument.  This is not 
        required.  If used, the values passed will be attempted to be 
        negotiated.  `key` can be of type `list`, `tuple`, `str` or 
        `None`
        
        ::
        
            @returns.json(key=...)
            @get(path='/get')
            def get_(self, **kwargs): pass
        """
        self.status_code = self.Adaptable(context=AliasReturnType.STATUS_CODE)
        """The response's status code can be exclusively returned

        ::
        
            @returns.status_code
            @post(path='/post')
            def post_(self, **kwargs): pass
        """
        self.text = self.Adaptable(context=AliasReturnType.TEXT)
        """The response's text representation can be exclusively 
        returned

        ::
        
            @returns.text
            @delete(path='/delete')
            def delete_(self, **kwargs): pass
        """

    class Json(_Context):

        def __init__(
                self, context: AliasReturnType = AliasReturnType.JSON, **kwargs
        ) -> None:
            super().__init__(context=context, **kwargs)

        def __call__(
                self, func: Optional[Callable] = None, **kwargs
        ) -> Callable:
            if not func:
                return self.__class__(**kwargs)
            return super().__call__(func=func)

    class Adaptable(_Context):

        def __init__(self, context: AliasReturnType, **kwargs) -> None:
            super().__init__(context=context, **kwargs)


class Sends:
    __slots__ = ('form_url_encoded', 'json',)

    def __init__(self):
        self.form_url_encoded = self.Adaptable(context=AliasSendsType.DATA)
        """Default to sending form-encoded data in the request

        ::
        
            @sends.form_url_encoded
            @post(path='/post')
            def post_data(self, body: Body): pass
        """
        self.json = self.Adaptable(context=AliasSendsType.JSON)
        """Default to sending JSON data in the request.

        ::
        
            @sends.json
            @post(path='/post')
            def post_json(self, body: Body): pass
        """

    class Adaptable(_Context):

        def __init__(self, context: AliasSendsType, **kwargs) -> None:
            super().__init__(context=context, **kwargs)


returns = Returns()
"""Provides access to decorators that allow a method to default to 
returning JSON, text or status code when invoked.  Declaring a 
subsequent return type will overwrite a previous declared return 
type."""
sends = Sends()
"""Provides access to decorators that allow a method to default to 
sending form-encoded data or JSON.  Declaring a subsequent send type 
will overwrite a previous declared send type."""
