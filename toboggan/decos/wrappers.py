# Local
from toboggan.aliases import AliasReturnType, AliasSendsType
from toboggan.annotations import Body, Options, Path, Query, QueryKebab
from toboggan.interfaces import InterfaceWrappers
from toboggan.models import (
    TypeHeadersDump,
    TypeNestedDump,
    TypeQueryParams,
    TypeSendDataDump,
    TypeSendJsonDump,
)

__all__ = ('Wrappers',)


class Wrappers(InterfaceWrappers):

    @staticmethod
    def _get_nested(json, value):
        orig = json
        if json and value:
            keys = (value,) if isinstance(value, str) else value
            for key in keys:
                try:
                    json = json[key]
                except (KeyError, TypeError,):
                    return TypeNestedDump(
                        sequence_expected=list(value),
                        sequence_found=list(orig.keys())
                    )._asdict()
        return json

    @staticmethod
    def _kebabize(key):
        return key.replace('_', '-')

    @staticmethod
    def _resolve_options(kw_dump):
        for key, val in kw_dump.items():
            if val.get('sig_type') is Options and val.get('kw_value'):
                return val.get('kw_value')
        return {}

    @staticmethod
    def _resolve_headers(conn, ctx_headers_value):
        base = {}
        if base_headers := getattr(conn, 'base_headers', None):
            base.update(base_headers)
        if ctx_headers_value:
            base.update(ctx_headers_value)
        return TypeHeadersDump(base)._asdict() if base else {}

    @staticmethod
    def _resolve_path_params(kw_dump, path):
        params = [
            {key: val.get('kw_value')} for key, val in kw_dump.items()
            if val.get('sig_type') is Path and val.get('kw_value')
        ]
        if params:
            resolved = {}
            for param in params:
                resolved.update(param)
            return path.format(**resolved)
        return path

    @staticmethod
    def _resolve_send(kw_dump, ctx_sends_type = None):
        body = next(
            (obj for obj in kw_dump.values() if obj.get('sig_type') is Body),
            None
        )
        if body:
            if ctx_sends_type and ctx_sends_type is AliasSendsType.DATA:
                return TypeSendDataDump(body.get('kw_value'))._asdict()
            return TypeSendJsonDump(body.get('kw_value'))._asdict()
        return {}

    def _resolve_query_params(self, conn, ctx_query_params_value, kw_dump):
        base = {}
        if base_query_params := getattr(conn, 'base_query_params', None):
            base.update(base_query_params)
        if ctx_query_params_value:
            base.update(ctx_query_params_value)
        for key, val in kw_dump.items():
            if val.get('sig_type') is Query and val.get('kw_value'):
                base[key] = val.get('kw_value')
            elif val.get('sig_type') is QueryKebab and val.get('kw_value'):
                base[self._kebabize(key)] = val.get('kw_value')
        if base:
            print(base)
            return TypeQueryParams(base)._asdict()
        return base

    def _resolve_response_sync(
            self,
            response,
            ctx_returns_type = None,
            ctx_returns_json_key = None
    ):
        if ctx_returns_type is AliasReturnType.JSON:
            json = response.json()
            if ctx_returns_json_key:
                if ctx_returns_json_key:
                    return self._get_nested(json, ctx_returns_json_key)
            return json
        elif ctx_returns_type is AliasReturnType.STATUS_CODE:
            return response.status_code
        elif ctx_returns_type is AliasReturnType.TEXT:
            return response.text
        return response

    async def _resolve_response_async(
            self,
            response,
            ctx_returns_type = None,
            ctx_returns_json_key = None
    ):
        if ctx_returns_type is AliasReturnType.JSON:
            json = await response.json()
            if ctx_returns_json_key:
                return self._get_nested(json, ctx_returns_json_key)
            return json
        elif ctx_returns_type is AliasReturnType.STATUS_CODE:
            return response.status
        elif ctx_returns_type is AliasReturnType.TEXT:
            return await response.text()
        return response

    async def wrapper_async(
            self,
            conn,
            method,
            path,
            kw_dump,
            ctx_headers_value = None,
            ctx_query_params_value = None,
            ctx_sends_type = None,
            ctx_returns_type = None,
            ctx_returns_json_key = None,
            **kwargs
    ):
        path = self._resolve_path_params(kw_dump, path)
        headers = self._resolve_headers(conn, ctx_headers_value)
        query_params = self._resolve_query_params(
            conn, ctx_query_params_value, kw_dump
        )
        send = self._resolve_send(kw_dump, ctx_sends_type)
        options = self._resolve_options(kw_dump)
        async with conn.session().request(
                method=method,
                url=conn.base_url + path,
                **options,
                **headers,
                **send,
                **query_params,
                **kwargs
        ) as response:
            return await self._resolve_response_async(
                response, ctx_returns_type, ctx_returns_json_key
            )

    def wrapper_sync(
            self,
            conn,
            method,
            path,
            kw_dump,
            ctx_headers_value = None,
            ctx_query_params_value = None,
            ctx_sends_type = None,
            ctx_returns_type = None,
            ctx_returns_json_key = None,
            **kwargs
    ):
        path = self._resolve_path_params(kw_dump, path)
        headers = self._resolve_headers(conn, ctx_headers_value)
        query_params = self._resolve_query_params(
            conn, ctx_query_params_value, kw_dump
        )
        send = self._resolve_send(kw_dump, ctx_sends_type)
        options = self._resolve_options(kw_dump)
        with conn.session() as session:
            response = session.request(
                method=method,
                url=conn.base_url + path,
                **options,
                **headers,
                **send,
                **query_params,
                **kwargs
            )
        return self._resolve_response_sync(
            response, ctx_returns_type, ctx_returns_json_key
        )
