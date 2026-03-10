# Standard
from asyncio import sleep as sleep_async
from time import sleep as sleep_sync
from typing import Any, Dict, List, Optional, Tuple, Union

# Local
from .responses import Responses
from .utils import _merge_mappings
from toboggan.aliases import AliasReturnType, AliasSessionType
from toboggan.models import TypeRetryDump, TypeRetryErrDump

__all__ = ('Requests',)


class Requests(Responses):
    __slots__ = (
        '__client_type',
        '__headers',
        '__method',
        '__options',
        '__query_params',
        '__retry',
        '__returns_json_key',
        '__returns_type',
        '__send',
        '__session',
        '__url',
    )

    def __init__(
            self,
            client_type: AliasSessionType,
            session: Any,
            method: str,
            url: str,
            headers: Dict,
            query_params: Dict,
            send: Dict,
            options: Dict,
            eval_type: Any,
            retry: Optional[TypeRetryDump] = None,
            returns_type: Optional[AliasReturnType] = None,
            returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None,
            **kwargs
        ):
        self.__client_type = client_type
        self.__session = session
        self.__method = method
        self.__url = url
        self.__headers = headers
        self.__query_params = query_params
        self.__send = send
        self.__options = options
        self.__retry = retry
        self.__returns_type = returns_type
        self.__returns_json_key = returns_json_key
        _merge_mappings(base=self.__headers, supp=self.__options, target='headers')
        _merge_mappings(base=self.__query_params, supp=self.__options, target='params')
        super().__init__(eval_type=eval_type)
    
    def __staged_request(self):
        request = self.__session.request(
            method=self.__method,
            url=self.__url,
            **self.__options,
            **self.__headers,
            **self.__send,
            **self.__query_params
        )
        return request
    
    def __request_sync(self) -> Union[Any, dict, int, str, None]:
        response = self.__staged_request()
        if self.__retry and response.status_code in self.__retry.status_forcelist:
            for attempt in range(self.__retry.total):
                backoff = self.__retry.backoff_factor * (2 ** attempt)
                sleep_sync(backoff)
                if attempt == self.__retry.total - 1:
                    err = TypeRetryErrDump(
                        status_code=response.status_code,
                        config=self.__retry
                    )
                    raise RuntimeError(err)
                response = self.__staged_request()
        resolved_response = self.resolve_response_std(
            response=response,
            ctx_returns_type=self.__returns_type,
            ctx_returns_json_key=self.__returns_json_key
        )
        return self.evaluate(response=resolved_response)
    
    async def __request_async(self) -> Union[Any, dict, int, str, None]:
        response = await self.__staged_request()
        if self.__retry and response.status in self.__retry.status_forcelist:
            for attempt in range(self.__retry.total):
                backoff = self.__retry.backoff_factor * (2 ** attempt)
                await sleep_async(backoff)
                if attempt == self.__retry.total - 1:
                    err = TypeRetryErrDump(
                        status_code=response.status,
                        config=self.__retry
                    )
                    raise RuntimeError(err)
                response = await self.__staged_request()
        if self.__client_type is AliasSessionType.AIOHTTP:
            resolved_response = self.resolve_response_awaitable(
                response=response,
                ctx_returns_type=self.__returns_type,
                ctx_returns_json_key=self.__returns_json_key
            )
            response = await resolved_response
            return self.evaluate(response=response)
        resolved_response = self.resolve_response_std(
            response=response,
            ctx_returns_type=self.__returns_type,
            ctx_returns_json_key=self.__returns_json_key
        )
        return self.evaluate(response=resolved_response)
    
    def resolve_request(self):
        if self.__client_type in (
            AliasSessionType.AIOHTTP, AliasSessionType.HTTPX_ASYNC
        ):
            return self.__request_async()
        return self.__request_sync()
