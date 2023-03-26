# Standard
from typing import Dict, NewType, Text, Union

__all__ = ('Body', 'QueryParam', 'PathParam',)

# Annotation used for a request body.
Body = NewType('RequestBody', Union[Dict, Text])
# Annotation used for a query parameter.
QueryParam = NewType('QueryParam', Text)
# Annotation used for a query parameters mapping.
QueryParamsMapping = NewType('QueryParamsMapping', Dict)
# Annotation used for a path parameter.
PathParam = NewType('PathParam', Text)
