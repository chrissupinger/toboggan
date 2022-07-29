from requests import Request


class SendBlock:

	_resp = None

	def __init__(self, session, request, settings):

		self._resp = session.send(session.prepare_request(Request(**request)), **settings)

	@property
	def data(self):

		return self._resp


class RequestorProps:

	@property
	def payload(self):

		return self._payload

	@property
	def request(self):

		body = dict(
			method=self.payload.method,
			url=self.payload.url,
			headers=self.payload.headers,
			auth=self.payload.auth
		)

		if isinstance(self.payload.body, str):

			body['data'] = self.payload.body

		elif isinstance(self.payload.body, dict):

			body['json'] = self.payload.body

		return body

	@property
	def status_code(self):

		return self.resp.status_code

	@property
	def headers(self):

		return self.resp.headers

	@property
	def json(self):

		return self.resp.json()


class Requestor(RequestorProps, SendBlock):

	def __init__(self, payload, payload_inspector):

		self._payload = payload

		super().__init__(payload.session, self.request, payload.settings)

		if payload_inspector:

			print(payload)

		self.resp = super().data
