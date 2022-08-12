from typing import Type


class HeadersConstructor:

	def __call__(self, connector):
		def arg_handler(*args, **kwargs):
			if isinstance(connector, Type):
				connector.headers = self.headers
			else:
				kwargs.update(dict(headers=self.headers))
			return connector(*args, **kwargs)
		return arg_handler


class HeadersProps:

	@property
	def headers(self):
		return self._headers


class Headers(HeadersProps, HeadersConstructor):

	def __init__(self, headers: dict):
		self._headers = headers
