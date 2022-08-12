import asyncio
from .models import NonblockTasks, NonblockResponse, NonblockResponses


class NonblockRequestorProps:

	@property
	def responses(self):
		return self._nonblock_responses.responses


class SendNonblock:

	@staticmethod
	async def send(self, session, request):
		response = NonblockResponse()
		async with session.request(**request) as resp:
			response.status_code = resp.status
			response.json = await resp.json()
			return response


class NonblockRequestor(NonblockRequestorProps):

	def __init__(self, requestPool):
		self.pool = requestPool
		self._nonblock_tasks, self._nonblock_responses = (
			NonblockTasks(), NonblockResponses())

	async def send_pool(self):
		async with self.pool.client(**self.pool.settings) as session:
			for request in self.pool.requests:
				self._nonblock_tasks.tasks = asyncio.ensure_future(
					SendNonblock.send(self, session, request))
			requestObjs = await asyncio.gather(*self._nonblock_tasks.tasks)
			for obj in requestObjs:
				self._nonblock_responses.responses = obj
