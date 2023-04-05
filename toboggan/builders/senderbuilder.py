# Standard
from typing import Tuple

# Third-party
from aiohttp import ClientResponse, ClientSession
from requests import Request, Response, Session, exceptions

# Local
from ..models import ResponseContext as _ResponseContext

__all__ = ('SenderBuilder',)


class SenderBuilder:
    
    def __init__(self, session, state):
        if isinstance(session, Session):
            self.response = self.Sender.blocking_fetch(session, state)
        elif isinstance(session, ClientSession):
            self.response = self.Sender.nonblocking_fetch(session, state)
    
    class Sender:
    
        def __init__(self, session, state):
            self.session = session
            self.state = state
        
        @classmethod
        def blocking_fetch(cls, session, state):
            prepped = session.prepare_request(Request(**state.request_config))
            return session.send(prepped)
        
        @classmethod
        async def nonblocking_fetch(cls, session, state):
            async with session.request(**state.request_config) as response:
                return response.status, await response.text(), await response.json()
    
    class BlockingResponse(_ResponseContext):
        
        def __init__(self, response: Response):
            super().__init__(response.status_code, response.text)
            try:
                json = response.json()
                self._json = json
            except exceptions.JSONDecodeError:
                pass
    
    class NonblockingResponse(_ResponseContext):
        
        def __init__(self, response: Tuple[ClientResponse.status, ClientResponse.text, ClientResponse.json]):
            super().__init__(*response)
    
    @classmethod
    def get_blocking_response(cls, session, state):
        return cls.BlockingResponse(cls.Sender.blocking_fetch(session, state))
    
    @classmethod
    async def get_nonblocking_response(cls, session, state):
        return cls.NonblockingResponse(await cls.Sender.nonblocking_fetch(session, state))
        