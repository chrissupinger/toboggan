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
	def request_settings(self):
		return self._request_settings

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
	def request_config(self):
		req = dict(
			method=self.method, url=self.url, headers=self.headers, auth=self.auth)
		if isinstance(self.body, str):
			req['data'] = self.body
		elif isinstance(self.body, dict):
			req['json'] = self.body
		if self.request_settings:
			for key, value in self.request_settings.items():
				req[key] = value
		return req

	@property
	def session_settings(self):
		return self.connector.settings


class PayloadTemplate(PayloadProps):

	def __init__(self, connector, request, method, request_settings):
		self._connector = connector
		self._request = request
		self._method = method
		self._request_settings = request_settings


class Payload(PayloadTemplate):

	def __init__(self, connector, request, method, request_settings):
		super().__init__(connector, request, method, request_settings)

	def __repr__(self):
		return str(
			'\nPAYLOAD INSPECTOR\n'
			f'{"-" * 25}\n'
			f'method:  {self.method}\n'
			f'path:    /{self.path}\n'
			f'base:    {self.connector.base}\n'
			f'headers: {self.headers}\n'
			f'body:    {self.body}\n'
			f'{"-" * 25}\n'
		)
