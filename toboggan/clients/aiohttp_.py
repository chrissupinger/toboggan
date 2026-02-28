# Standard
from typing import Dict, List, Optional, Tuple, Union

# Third-party
from aiohttp import ClientResponse, ClientSession

# Local
from .resolvers import _get_nested, _merge_mappings
from toboggan.aliases import AliasReturnType


class ConfigAiohttp:
    __slots__ = ()

    @staticmethod
    async def _resolve_response(
            response: ClientResponse,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None
    ) -> Union[ClientResponse, Dict, str, int]:
        if ctx_returns_type is AliasReturnType.JSON:
            json = await response.json()
            if ctx_returns_json_key:
                return _get_nested(json=json, value=ctx_returns_json_key)
            return json
        elif ctx_returns_type is AliasReturnType.STATUS_CODE:
            return response.status
        elif ctx_returns_type is AliasReturnType.TEXT:
            return await response.text()
        return response

    async def request(
            self,
            session: ClientSession,
            method: str,
            url: str,
            headers: Dict,
            query_params: Dict,
            send: Dict,
            options: Dict,
            returns_type: Optional[AliasReturnType] = None,
            returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None,
            **kwargs
    ) -> Union[ClientResponse, dict, int, str, None]:
        _merge_mappings(base=headers, supp=options, target='headers')
        _merge_mappings(base=query_params, supp=options, target='params')
        async with session.request(
                method=method,
                url=url,
                **options,
                **headers,
                **send,
                **query_params,
                **kwargs
        ) as response:
            resolved_response = self._resolve_response(
                response=response,
                ctx_returns_type=returns_type,
                ctx_returns_json_key=returns_json_key
            )
            return await resolved_response


aiohttp_ = ConfigAiohttp()
