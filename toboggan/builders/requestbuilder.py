# Standard
from functools import cached_property
from typing import Dict, Optional, Text

# Local
from ..models import DecoCommonContext, MethodContext, RequestCommonContext
from ..utils import exceptions

__all__ = ('RequestBuilder',)


class RequestBuilder:

    class State:

        def __init__(self, blocking, nonblocking, headers, query, method):
            self.blocking: Optional = blocking
            self.nonblocking: Optional = nonblocking
            self.headers: Optional[DecoCommonContext] = headers
            self.query: Optional[DecoCommonContext] = query
            self.method: Optional[MethodContext] = method

        @cached_property
        def abs_url(self):
            path = self.method.path_w_params
            if self.blocking:
                base = self.blocking.base_url
            elif self.nonblocking:
                base = self.nonblocking.base_url
            else:
                raise exceptions.NoBaseUrl()
            if base.endswith('/'):
                base = base.rstrip('/')
            if path:
                if path.startswith('/'):
                    path = path.replace('/', '', 1)
            return '/'.join((base, path,))

        @classmethod
        def stage(cls, blocking=None, nonblocking=None, headers=None, query=None, method=None):
            return cls(blocking, nonblocking, headers, query, method)

    class Config(RequestCommonContext):

        def __init__(self, state):
            super().__init__()
            self.method = state.method.verb
            self.url = state.abs_url
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
    def get_state(cls, mapping):
        return cls.Config(cls.State.stage(**mapping))
