# Standard
from typing import Iterable
from urllib.parse import urlparse

__all__ = (
    'InvalidBaseUrl',
    'InvalidClassDecoChain',
    'InvalidScheme',
    'InvalidSessionSetting',
    'NoVerb',)


class InvalidBaseUrl(Exception):

    def __init__(self, base_url: urlparse) -> None:
        message: str = \
            'Parameter `base_url` is either missing or is invalid.  ' \
            f'Parsed: {base_url}.'
        super().__init__(message)


class InvalidClassDecoChain(Exception):

    def __init__(self, alias: str, valid_aliases: Iterable):
        message: str = \
            f'A `{alias}` decorator is not valid for use with classes.  ' \
            f'Valid class decorators: {", ".join(valid_aliases)}.'
        super().__init__(message)


class InvalidScheme(Exception):

    def __init__(self, base_url: urlparse, valid_schemes: Iterable) -> None:
        message: str = \
            'The scheme for the `base_url` parameter is either missing or ' \
            f'is invalid.  Parsed: {base_url}.  Valid schemes: ' \
            f'{", ".join(valid_schemes)}.'
        super().__init__(message)


class InvalidSessionSetting(Exception):
    """Raised when an invalid session setting has been provided.
    """

    def __init__(self, setting: str, valid_settings: Iterable) -> None:
        message: str = \
            f'Parameter `{setting}` is an invalid setting for this session ' \
            f'type.  Valid parameters: {", ".join(valid_settings)}.'
        super().__init__(message)


class InvalidType(Exception):

    def __init__(
            self, parameter: str, type_: str, allowed_types: Iterable) -> None:
        message: str = \
            f'The `{parameter}` parameter is annotated as a `{type_}` ' \
            f'type.  Allowed types for this annotation are: ' \
            f'{", ".join([str(type_) for type_ in allowed_types])}.'
        super().__init__(message)


class NoVerb(Exception):

    def __init__(self, verbs: Iterable) -> None:
        message: str = \
            'No verb has been declared.  Valid verbs are: ' \
            f'{", ".join(verbs)}.  Decorate your methods using `@` and a ' \
            'valid verb (i.e., @get(...); @post(...); @put(...); etc.).'
        super().__init__(message)
