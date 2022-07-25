import asyncio
from aiohttp import ClientSession
from requests import Request, Session


class Send:

	@staticmethod
	def block(client, request, settings):

		return client.send(client.prepare_request(Request(**request)), **settings)

	@staticmethod
	async def nonblock(client, request, settings):

		async with getattr(client, None.lower())(url=None) as resp:

			return await resp


class RequestorProps:

	@property
	def payload(self):

		return self._payload

	@property
	def blockRequest(self):

		return dict(
			method=self.payload.method,
			url=self.payload.url,
			json=self.payload.json,
			headers=self.payload.headers
		)

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

	def __init__(self, payload, payload_inspector=False):

		self._payload = payload

		if payload_inspector:

			print(payload)

		if isinstance(payload.connector.client, Session):

			self.resp = Send.block(
				client=payload.connector.client,
				request=self.blockRequest,
				settings=payload.connector.blockSettings
			)

		elif isinstance(payload.connector.client, ClientSession):

			...
