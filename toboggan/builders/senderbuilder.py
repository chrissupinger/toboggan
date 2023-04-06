# Standard
from typing import Dict, Optional, Text, Tuple, Union

# Third-party
from aiohttp import ClientResponse, ClientSession
from requests import Request, Response, Session, exceptions

# Local
from ..models import ResponseContext as _ResponseContext

__all__ = ('SenderBuilder',)


class SenderBuilder:
    
    def __init__(self, session: Union[Session, ClientSession], state):
        if isinstance(session, Session):
            self.response = self.Sender.blocking_fetch(session, state)
        elif isinstance(session, ClientSession):
            self.response = self.Sender.nonblocking_fetch(session, state)
    
    class Sender:
    
        def __init__(self, session, state):
            self.session = session
            self.state = state
        
        @classmethod
        def blocking_fetch(cls, session: Session, state) -> Response:
            prepped = session.prepare_request(Request(**state.request_config))
            return session.send(prepped)
        
        @classmethod
        async def nonblocking_fetch(cls, session: ClientSession, state) -> Tuple[int, Optional[Text], Optional[Dict]]:
            async with session.request(**state.request_config) as response:
                status = response.status
                text = await response.text()
                json = await response.json()
                return status, text, json
    
    class BlockingResponse(_ResponseContext):
        
        def __init__(self, response: Response):
            super().__init__(status_code=response.status_code, text=response.text)
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
        