class PayloadProps:

	@property
	def connector(self):

		return self._connector

	@property
	def request(self):

		return self._request

	@property
	def method(self):

		return self._method

	@property
	def session(self):

		return self.connector.client

	@property
	def path(self):

		return self.request.get('path').format(**self.request)

	@property
	def url(self):

		if self.path:

			return f"{self.connector.base}/{self.path}"

		return self.connector.base

	@property
	def body(self):

		return self.request.get('body')

	@property
	def headers(self):

		if self.connector.headers and self.request.get('headers'):

			return {**self.connector.headers, **self.request.get('headers')}

		elif self.connector.headers:

			return self.connector.headers

		elif self.request.get('headers'):

			return self.request.get('headers')

		else:

			pass

	@property
	def auth(self):

		return self.connector.auth

	@property
	def blockSettings(self):

		return self.connector.blockSettings


class Payload(PayloadProps):

	def __init__(self, connector, request, method):

		self._connector = connector
		self._request = request
		self._method = method

	def __repr__(self):

		return str(
			'\nPAYLOAD INSPECTOR\n'
			f'{"-" * 25}\n'
			f'method:  {self.method}\n'
			f'path:    /{self.request.get("path")}\n'
			f'base:    {self.connector.base}\n'
			f'headers: {self.headers}\n'
			f'body:    {self.json}\n'
			f'{"-" * 25}\n'
		)
