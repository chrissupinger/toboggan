# Standard
from functools import cached_property
from typing import Dict, Optional, Text, Tuple

# Third-party
from aiohttp import ClientSession
from multidict import CIMultiDictProxy
from requests import Request, Session, exceptions

# Local
from ..models import BlockingContext, NonblockingContext, ResponseContext, YieldsContext
from ..utils import YieldsAliases

__all__ = ('MessageBuilder',)


class MessageBuilder:

    class _Request:
        
        @staticmethod
        def _get_json(response):
            try:
                return response.json()
            except (exceptions.JSONDecodeError, Exception,) as err_msg:
                return dict(error=err_msg)

        @classmethod
        def blocking(cls, session: Session, settings: BlockingContext):
            prepped = session.prepare_request(Request(**settings.request_config))
            response = session.send(prepped)
            status = response.status_code
            headers = response.headers
            text = response.text
            json = cls._get_json(response)
            return status, headers, text, json

        @classmethod
        async def nonblocking(
                cls,
                session: ClientSession,
                settings: NonblockingContext) -> Tuple[int, Optional[CIMultiDictProxy], Optional[Text], Optional[Dict]]:
            async with session.request(**settings.request_config) as response:
                status = response.status
                headers = response.headers
                text = await response.text()
                json = await cls._get_json(response=response)
                return status, headers, text, json

    class _Response(ResponseContext):

        def __init__(self, response, yields):
            super().__init__(*response, yields=yields)
        
        @staticmethod
        def _get_nested(json, keys):
            for key in keys:
                try:
                    json = json[key]
                except KeyError:
                    return None
            return json
    
        @cached_property
        def message(self):
            if self._yields:
                if self._yields.type_ == YieldsAliases.json.name:
                    if self._yields.values:
                        return self._get_nested(json=self._json, keys=self._yields.values)
                    return self._json
                if self._yields.type_ == YieldsAliases.text.name:
                    return self.text
            return self

    @classmethod
    def send_blocking_request(cls, session, settings, yields: YieldsContext):
        return cls._Response(cls._Request.blocking(session, settings), yields).message

    @classmethod
    async def send_nonblocking_request(cls, session, settings, yields: YieldsContext):
        return cls._Response(await cls._Request.nonblocking(session, settings), yields).message
