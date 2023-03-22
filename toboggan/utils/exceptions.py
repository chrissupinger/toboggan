# Standard
from typing import Iterable, Text

__all__ = ('InvalidSessionSetting',)


class InvalidSessionSetting(Exception):
    """Raised when an invalid session setting has been provided.
    """

    def __init__(self, setting: Text, valid_settings: Iterable,):
        self.message = 'Argument `{}` is an invalid setting for a session.  Valid arguments: {}'
        super().__init__(self.message.format(setting, ', '.join(valid_settings)))
