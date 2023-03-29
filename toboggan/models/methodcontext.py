# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional, Text, Union

# Local
from ..utils import Body, ContextAliases, QueryParam


@dataclass(slots=True, init=True)
class MethodContext:
    alias: Optional[Text] = field(default=ContextAliases.method.name)
    verb: Optional[Text] = field(default=None)
    path: Optional[Text] = field(default=None)
    path_params: Optional[Dict] = field(default=None)
    query: Optional[Dict] = field(default_factory=dict)
    body: Optional[Union[Dict, Text]] = field(default=None)

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, verb={self.verb}, path={self.path_w_params}, body={self.body})'

    def set_method_from_args(self, params: Dict, annotations: Dict) -> None:
        if annotations:
            for key, val in annotations.items():
                if val.__qualname__ == Body.__qualname__:
                    self.body = params.get(key)
                if val.__qualname__ == QueryParam.__qualname__:
                    self.query.update(params)

    @property
    def path_w_params(self):
        return self.path.format(**self.path_params)
