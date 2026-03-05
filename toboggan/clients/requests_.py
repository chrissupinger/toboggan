# Standard
from time import sleep
from typing import Dict, List, Optional, Tuple, Union

# Third-party
from requests import Response, Session

# Local
from .resolvers import _get_nested, _merge_mappings
from toboggan.aliases import AliasReturnType
from toboggan.models import TypeRetryDump, TypeRetryErrDump

class ConfigRequests:
    __slots__ = ()

    @staticmethod
    def _resolve_response(
            response: Response,
            ctx_returns_type: Optional[AliasReturnType] = None,
            ctx_returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None
    ) -> Union[Response, Dict, str, int]:
        if ctx_returns_type is AliasReturnType.JSON:
            json = response.json()
            if ctx_returns_json_key:
                if ctx_returns_json_key:
                    return _get_nested(json=json, value=ctx_returns_json_key)
            return json
        elif ctx_returns_type is AliasReturnType.STATUS_CODE:
            return response.status_code
        elif ctx_returns_type is AliasReturnType.TEXT:
            return response.text
        return response

    def request(
            self,
            session: Session,
            method: str,
            url: str,
            headers: Dict,
            query_params: Dict,
            send: Dict,
            options: Dict,
            retry: Optional[TypeRetryDump] = None,
            returns_type: Optional[AliasReturnType] = None,
            returns_json_key: Optional[Union[str, List[str], Tuple[str]]] = None,
            **kwargs
    ) -> Union[Response, dict, int, str, None]:
        _merge_mappings(base=headers, supp=options, target='headers')
        _merge_mappings(base=query_params, supp=options, target='params')
        with session:
            staged_request = lambda: session.request(
                method=method,
                url=url,
                **options,
                **headers,
                **send,
                **query_params,
                **kwargs
            )
            response = staged_request()
            if retry and response.status_code in retry.status_forcelist:
                for attempt in range(retry.total):
                    backoff = retry.backoff_factor * (2 ** attempt)
                    sleep(backoff)
                    if attempt == retry.total - 1:
                        err = TypeRetryErrDump(
                            status_code=response.status_code,
                            config=retry
                        )
                        raise RuntimeError(err)
                    response = staged_request()
        resolved_response = self._resolve_response(
            response=response,
            ctx_returns_type=returns_type,
            ctx_returns_json_key=returns_json_key
        )
        return resolved_response


requests_ = ConfigRequests()
