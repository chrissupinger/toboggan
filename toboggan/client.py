# Third-party
from aiohttp import ClientSession
from requests import Session

# Local
from .models import SessionContext as _SessionContext
from .utils import InvalidSessionSetting

__all__ = ('Client',)


class Client:

    class SessionState(_SessionContext):

        def __init__(self, session, settings):
            super().__init__(session, settings)

        @classmethod
        def stage(cls, session, settings):
            return cls(session, settings)

    @classmethod
    def block(cls, session=Session, **kwargs):
        session_state = cls.SessionState.stage(session=session(), settings=kwargs)
        _attrs = session.__attrs__
        for key, val in kwargs.items():
            if key not in _attrs:
                raise InvalidSessionSetting(setting=key, valid_settings=_attrs)
            setattr(session_state.session, key, val)
        return session_state

    @classmethod
    def nonblock(cls, session=ClientSession, **kwargs):
        session_state = cls.SessionState.stage(session=session, settings=kwargs)
        _attrs = session.__init__.__annotations__.keys()
        for key, val in kwargs.items():
            if key not in _attrs:
                raise InvalidSessionSetting(setting=key, valid_settings=_attrs)
        return session_state
