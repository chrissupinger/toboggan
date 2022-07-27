import asyncio
from aiohttp import ClientSession
from requests import Request, Session


class Send:

	@staticmethod
	def block(session, request, settings):

		return session.send(session.prepare_request(Request(**request)), **settings)

	@staticmethod
	async def nonblock(session, request, settings):

		async with getattr(session, None.lower())(url=None) as resp:

			return await resp


class RequestorProps:

	@property
	def payload(self):

		return self._payload

	@property
	def blockRequest(self):

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


class Requestor(RequestorProps, Send):

	def __init__(self, payload, payload_inspector):

		self._payload = payload

		if payload_inspector:

			print(payload)

		if isinstance(payload.session, Session):

			self.resp = Send.block(
				session=payload.session,
				request=self.blockRequest,
				settings=payload.blockSettings
			)

		elif isinstance(payload.session, ClientSession):

			...
