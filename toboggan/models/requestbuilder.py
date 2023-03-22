# Standard
from collections import OrderedDict
from functools import cached_property
from typing import Dict, Optional, Text

# Third-party
from requests import Request

# Local
from .commoncontext import CommonContext
from .methodcontext import MethodContext

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
    def blocking_response(cls, mapping):
        """Not yet implemented: files, auth, cookies, hooks
        """
        state = cls.State.stage(**mapping)
        base_request = Request(method=state.method.verb, url=state.abs_url)
        if state.headers:
            for key, val in state.headers.values.items():
                base_request.headers[key] = val
        if state.method.body:
            if isinstance(state.method.body, Dict):
                base_request.json = state.method.body
            elif isinstance(state.method.body, Text):
                base_request.data = state.method.body
        if state.query:
            for key, val in state.query.values.items():
                base_request.params[key] = val
        prepped_request = state.blocking.client.session.prepare_request(base_request)
        try:
            return state.blocking.client.session.send(prepped_request)
        except Exception as err_msg:
            return err_msg

    @classmethod
    def nonblocking_future(cls, mapping):
        state = cls.State.stage(**mapping)
        base = OrderedDict()
        base['method'] = state.method.verb
        base['url'] = state.abs_url
        if state.headers:
            base['headers'] = state.headers.values
        if state.method.body:
            if isinstance(state.method.body, Dict):
                base['json'] = state.method.body
            elif isinstance(state.method.body, Text):
                base['data'] = state.method.body
        if state.query:
            base['params'] = state.query.values
        return base
