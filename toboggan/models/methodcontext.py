# Standard
from dataclasses import dataclass, field
from typing import Dict, Optional, Text, Union

# Local
from ..utils import Body, ContextAliases


@dataclass(slots=True, init=True)
class MethodContext:
    alias: Optional[Text] = field(default=ContextAliases.method.name)
    verb: Optional[Text] = field(default=None)
    path: Optional[Text] = field(default=None)
    path_params: Optional[Dict] = field(default=None)
    body: Optional[Union[Dict, Text]] = field(default=None)

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.alias}, verb={self.verb}, path={self.path_w_params}, body={self.body})'

    def add_body(self, params: Dict, annotations: Dict) -> None:
        if annotations:
            [body_param] = tuple(key for key, val in annotations.items() if val.__qualname__ == Body.__qualname__)
            self.body = params.get(body_param)

    @property
    def path_w_params(self):
        return self.path.format(**self.path_params)
