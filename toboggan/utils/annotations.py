# Standard
from typing import Dict, NewType, Text, Union

__all__ = ('Body', 'PathParam',)

# Annotation used for a request body.
Body = NewType('RequestBody', Union[Dict, Text])
# Annotation used for a path parameter.
PathParam = NewType('PathParam', Text)
