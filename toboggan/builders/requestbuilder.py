# Standard
from functools import cached_property
from typing import Dict, Optional, Text

# Third-party
from requests import Request

# Local
from ..models import CommonContext, MethodContext

__all__ = ('RequestBuilder',)


class RequestBuilder:

    class State:

        def __init__(self, blocking, nonblocking, headers, query, method):
            self.blocking: Optional = blocking
            self.nonblocking: Optional = nonblocking
            self.headers: Optional[CommonContext] = headers
            self.query: Optional[CommonContext] = query
            self.method: Optional[MethodContext] = method

        @cached_property
        def abs_url(self):
            base = self.blocking.base_url if self.blocking else (self.nonblocking.base_url if self.nonblocking else None)
            path = self.method.path_w_params
            if base.endswith('/'):
                base = base.rstrip('/')
            if path:
                if path.startswith('/'):
                    path = path.replace('/', '', 1)
            return '/'.join((base, path,))

        @classmethod
        def stage(cls, blocking=None, nonblocking=None, headers=None, query=None, method=None):
            return cls(blocking, nonblocking, headers, query, method)

    @classmethod
    def get_state(cls, mapping):
        state = cls.State.stage(**mapping)
        base = dict()
        base.update(dict(method=state.method.verb))
        base.update(dict(url=state.abs_url))
        if state.headers:
            base.update(dict(headers=state.headers.values))
        if state.method.body:
            if isinstance(state.method.body, Dict):
                base.update(dict(json=state.method.body))
            elif isinstance(state.method.body, Text):
                base.update(dict(data=state.method.body))
        if state.query:
            base.update(dict(params=state.query.values))
        return base
