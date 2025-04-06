from .annotations import Body, Path, Query, QueryKebab, QueryMap, QueryMapKebab
from .client import AiohttpClient, RequestsClient
from .connector import Connector
from .decos import (
    connect,
    delete,
    get,
    head,
    headers,
    options,
    params,
    patch,
    post,
    put,
    returns,
    sends,
    trace,)
from .models import ResponseObject
