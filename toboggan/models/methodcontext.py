# Standard
from typing import Dict, Optional, Text, Union

# Local
from ..utils import Body, ContextAliases, QueryParam


class MethodContext:
    __slots__ = ('alias', 'verb', 'path', 'path_params', 'query', 'body',)

    def __init__(
            self,
            verb: Optional[Text],
            path: Optional[Text], alias: Optional[Text] = ContextAliases.method.name,
            path_params: Optional[Dict] = None,
            body: Optional[Union[Dict, Text]] = None):
        self.alias = alias
        self.verb = verb
        self.path = path
        self.path_params = path_params
        self.query = dict()
        self.body = body

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, verb={self.verb}, path={self.path_w_params}, body={self.body})'

    def set_method_from_args(self, annotations: Dict) -> None:
        if annotations:
            for key, val in annotations.items():
                if val.__qualname__ == Body.__qualname__:
                    self.body = self.path_params.get(key)
                if val.__qualname__ == QueryParam.__qualname__:
                    self.query[key] = self.path_params.get(key)

    @property
    def path_w_params(self):
        return self.path.format(**self.path_params)
