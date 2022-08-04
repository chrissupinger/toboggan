from requests import Request, Session


class SendBlockProps:

	@property
	def status_code(self):

		return self._resp.status_code

	@property
	def headers(self):

		return self._resp.headers

	@property
	def json(self):

		return self._resp.json()


class SendBlock(SendBlockProps):

	def __init__(self, session, request, settings):

		self._resp = session.send(session.prepare_request(Request(**request)), **settings)


class RequestorProps:

	@property
	def payload(self):

		return self._payload

	@property
	def request(self):

		return self.payload.requestConfig


class BlockRequestor(RequestorProps, SendBlock):

	def __init__(self, payload):

		self._payload = payload

		super().__init__(payload.session, self.request, payload.sessionSettings)
