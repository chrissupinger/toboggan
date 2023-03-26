# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .models import ClientContext as _ClientContext
from .utils import exceptions

__all__ = ('Client',)


class Client:
    """Constructs the native toboggan clients.
    """

    class State(_ClientContext):
        """Constructs the elements required to form a toboggan client.
        """

        def __init__(self, session, settings):
            super().__init__(session, settings)

        @classmethod
        def stage(cls, session, settings):
            return cls(session, settings)

    @classmethod
    def block(cls, session=Session, **kwargs):
        """Invokes a blocking session using requests.Session and with the settings provided.
        """
        session_state = cls.State.stage(session=session(), settings=kwargs)
        _attrs = session.__attrs__
        # Checks for valid arguments IAW the client and its session.  If invalid parameter detected, raises
        # utils.exceptions.InvalidSessionSetting.
        for key, val in kwargs.items():
            if key not in _attrs:
                raise exceptions.InvalidSessionSetting(setting=key, valid_settings=_attrs)
            setattr(session_state.session, key, val)
        return session_state

    @classmethod
    def nonblock(cls, session=ClientSession, **kwargs):
        """Sets a nonblocking method (aiohttp.ClientSession) as the session and without invocation.  Also sets access to
        passed session settings.
        """
        session_state = cls.State.stage(session=session, settings=kwargs)
        _attrs = session.__init__.__annotations__.keys()
        # Checks for valid arguments IAW the client and its session.  If invalid parameter detected, raises
        # utils.exceptions.InvalidSessionSetting.
        for key, val in kwargs.items():
            if key not in _attrs:
                raise exceptions.InvalidSessionSetting(setting=key, valid_settings=_attrs)
        return session_state
