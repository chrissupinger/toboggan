# Standard
from typing import Iterable
from urllib.parse import urlparse

__all__ = (
    'InvalidBaseUrl', 'InvalidScheme', 'InvalidSessionSetting', 'NoVerb',)


class InvalidBaseUrl(Exception):

    def __init__(self, base_url: urlparse) -> None:
        self.__message: str = \
            'Parameter `base_url` is either missing or is invalid.  ' \
            f'Parsed: {base_url}.'
        super().__init__(self.__message)


class InvalidScheme(Exception):

    def __init__(self, base_url: urlparse, valid_schemes: Iterable) -> None:
        self.__message: str = \
            'The scheme for the `base_url` parameter is either missing or ' \
            f'is invalid.  Parsed: {base_url}.  Valid schemes: ' \
            f'{", ".join(valid_schemes)}.'
        super().__init__(self.__message)


class InvalidSessionSetting(Exception):
    """Raised when an invalid session setting has been provided.
    """

    def __init__(self, setting: str, valid_settings: Iterable) -> None:
        self.__message: str = \
            f'Parameter `{setting}` is an invalid setting for this session ' \
            f'type.  Valid parameters: {", ".join(valid_settings)}.'
        super().__init__(self.__message)


class NoVerb(Exception):

    def __init__(self, verbs: Iterable) -> None:
        self.__message: str = \
            'No verb has been declared.  Valid verbs are: ' \
            f'{", ".join(verbs)}.  Decorate your methods using `@` and a ' \
            'valid verb (i.e., @get(...); @post(...); @put(...); etc.).'
        super().__init__(self.__message)
