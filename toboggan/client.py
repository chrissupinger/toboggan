# Standard
from typing import Callable, Iterable, Union

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

    @staticmethod
    def _get_session_attrs(session: Union[Session, ClientSession]) -> Iterable:
        """Returns an iterable containing the attributes of a session.

        :param session: requests.Session or aiohttp.ClientSession
        """
        if isinstance(session, Session):
            return Session.__attrs__
        elif session == ClientSession:
            return ClientSession.__init__.__annotations__.keys()

    @classmethod
    def _set_session_state(cls, session: Union[Callable, Session], **kwargs) -> State.stage:
        """Sets session attributes if using a blocking session.  If a nonblocking session, sets a mapping to be
        consumed during session creation.

        :param session: requests.Session or aiohttp.ClientSession
        :param kwargs: requests.Session.__attrs__ or aiohttp.ClientSession.__init__.__annotations__.keys()
        """
        _attrs = cls._get_session_attrs(session)
        session_state = cls.State.stage(session=session, settings=kwargs)
        for key, val in kwargs.items():
            if key not in _attrs:
                raise exceptions.InvalidSessionSetting(setting=key, valid_settings=_attrs)
            if isinstance(session, Session):
                setattr(session_state.session, key, val)
        return session_state

    @classmethod
    def block(cls, **kwargs) -> _set_session_state:
        """Invokes a blocking session using requests.Session and with the settings provided.

        :param kwargs: headers, cookies, auth, proxies, hooks, params, verify, cert, adapters, stream, trust_env, max_redirects
        """
        return cls._set_session_state(session=Session(), **kwargs)

    @classmethod
    def nonblock(cls, **kwargs) -> _set_session_state:
        """Sets a nonblocking method (aiohttp.ClientSession) as the session and without invocation.  Also sets access to
        passed session settings.

        :param kwargs: base_url, connector, loop, cookies, headers, skip_auto_headers, auth, json_serialize, request_class, response_class, ws_response_class, version, cookie_jar, connector_owner, raise_for_status, read_timeout, conn_timeout, timeout, auto_decompress, trust_env, requote_redirect_url, trace_configs, read_bufsize, return
        """
        return cls._set_session_state(session=ClientSession, **kwargs)
