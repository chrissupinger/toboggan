# Standard
from typing import Iterable, Text

__all__ = ('InvalidSessionSetting', 'NoBaseUrl', 'UnrecognizedClientType', 'MissingRequestStateAttribute',)


class InvalidSessionSetting(Exception):
    """Raised when an invalid session setting has been provided.
    """

    def __init__(self, setting: Text, valid_settings: Iterable):
        self.message = 'Parameter `{}` is an invalid setting for a session.  '\
                       'Valid parameters: {}.'.format(setting, ', '.join(valid_settings))
        super().__init__(self.message)


class NoBaseUrl(Exception):
    """Raised when no base_url has been passed to the Connector.
    """

    def __init__(self):
        self.message = 'Parameter `base_url` is missing.  '\
                       'This is required to instantiate a Connector object.  '\
                       'This can be declared within a model or at instantiation.'
        super().__init__(self.message)


class UnrecognizedClientType(Exception):
    """Raised when a client is invalid or incompatible with toboggan.
    """

    def __init__(self, client):
        self.message = f'`{client}` is either invalid or incompatible.  '\
                       'Valid client types: toboggan.Client (block or nonblock), request.Session, aiohttp.ClientSession.  '\
                       'This is required to instantiate a Connector object.  '\
                       'This can be declared within a model or at instantiation.'
        super().__init__(self.message)


class MissingRequestStateAttribute(Exception):
    """Raised when the request builder does not receive required objects to create a request state.
    """

    def __init__(self, state_keys, valid_keys):
        self.message = 'State keys detected: {}.  '\
                       'Valid state keys: {}.'.format(', '.join(state_keys), ', '.join(valid_keys))
        super().__init__(self.message)
