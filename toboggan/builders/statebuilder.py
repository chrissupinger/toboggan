# Standard
from functools import cached_property
from types import MappingProxyType
from typing import Dict, Optional, Text, Tuple, Union

# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from ..models import (
    DecoCommonContext,
    MethodContext,
    YieldsContext,
    BlockingContext as _BlockingContext,
    NonblockingContext as _NonblockingContext)
from ..utils import exceptions

__all__ = ('StateBuilder',)


class StateBuilder:

    class State:

        def __init__(self, blocking, nonblocking, headers, query, method, yields):
            self.blocking: Optional = blocking
            self.nonblocking: Optional = nonblocking
            self.headers: Optional[DecoCommonContext] = headers
            self.query: Optional[DecoCommonContext] = query
            self.method: Optional[MethodContext] = method
            self.yields: Optional[YieldsContext] = yields

        @cached_property
        def abs_url(self) -> Text:
            path = self.method.path_w_params
            if self.blocking:
                base = self.blocking.base_url
            elif self.nonblocking:
                base = self.nonblocking.base_url
            else:
                raise exceptions.NoBaseUrl()
            base = base.rstrip('/') if base.endswith('/') else base
            if path:
                path = path.replace('/', '', 1) if path.startswith('/') else path
                return '/'.join((base, path,))
            return base

        @classmethod
        def stage(cls, blocking=None, nonblocking=None, headers=None, query=None, method=None, yields=None):
            return cls(blocking, nonblocking, headers, query, method, yields)

    class RequestConfig(_BlockingContext, _NonblockingContext):

        def __init__(self, state):
            if state.blocking:
                _BlockingContext.__init__(self, method=state.method.verb, url=state.abs_url)
            elif state.nonblocking:
                _NonblockingContext.__init__(self, method=state.method.verb, url=state.abs_url)
            self.set_request_config(state=state)
        
        def set_request_config(self, state):
            if state.headers:
                self.headers = state.headers.values
            if state.method.body:
                if isinstance(state.method.body, Dict):
                    self.json = state.method.body
                elif isinstance(state.method.body, Text):
                    self.data = state.method.body
            if state.query:
                for key, val in state.query.values.items():
                    self.params[key] = val
            if state.method.query:
                for key, val in state.method.query.items():
                    self.params[key] = val
                    
    @classmethod
    def get_state(
            cls,
            mapping: MappingProxyType
    ) -> Union[Tuple[Session, _BlockingContext, YieldsContext], Tuple[ClientSession, _NonblockingContext, YieldsContext]]:
        staged = cls.State.stage(**mapping)
        settings = cls.RequestConfig(staged)
        if staged.blocking:
            session = staged.blocking.session
        elif staged.nonblocking:
            session = staged.nonblocking.session
        else:
            raise exceptions.UnrecognizedClientType(client=Session)
        return session, settings, staged.yields
