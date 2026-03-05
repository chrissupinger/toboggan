from .connector import Connector
from .decos import (
    connect,
    delete,
    get,
    head,
    options,
    patch,
    post,
    put,
    trace,
)
"""Verbs"""
from .decos import headers, params, retry, returns, sends
"""Request and response"""
from .annotations import Body, Options, Path, Query, QueryKebab
"""Annotations"""
