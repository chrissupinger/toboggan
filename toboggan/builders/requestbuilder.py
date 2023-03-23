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

        @cached_property
        def request_config(self):
            base = dict()
            base.update(dict(method=self.method.verb))
            base.update(dict(url=self.abs_url))
            if self.headers:
                base.update(dict(headers=self.headers.values))
            if self.method.body:
                if isinstance(self.method.body, Dict):
                    base.update(dict(json=self.method.body))
                elif isinstance(self.method.body, Text):
                    base.update(dict(data=self.method.body))
            if self.query:
                base.update(dict(params=self.query.values))
            return base

        @classmethod
        def stage(cls, blocking=None, nonblocking=None, headers=None, query=None, method=None):
            return cls(blocking, nonblocking, headers, query, method)

    @classmethod
    def get_state(cls, mapping):
        state = cls.State.stage(**mapping)
        return state
