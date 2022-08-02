import asyncio
from .models import NonblockResponseModel


class NonblockRequestorProps:

	@property
	def responses(self):

		return self._responses


class SendNonblock:

	@staticmethod
	async def send(self, session, request):

		response = NonblockResponseModel()

		async with session.request(**request) as resp:

			response.status_code = resp.status
			response.json = await resp.json()

			return response


class NonblockRequestor(NonblockRequestorProps):

	def __init__(self, requestPool):

		self.pool = requestPool
		self._responses = list()

	async def sendPool(self):

		async with self.pool.client(**self.pool.settings) as session:

			tasks = [
				asyncio.ensure_future(SendNonblock.send(self, session, request))
				for request in self.pool.requests
			]

			requestObjs = await asyncio.gather(*tasks)

			for obj in requestObjs:

				self._responses.append(obj)
