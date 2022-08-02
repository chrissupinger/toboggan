import asyncio
from .nonblockrequestor import NonblockRequestor
from .models import NonblockRequestPoolModel


class StagingAreaProps:

	@property
	def responses(self):

		return self._responses


class StagingArea(StagingAreaProps):

	def __init__(self, client, auth, settings):

		self.requestPool = NonblockRequestPoolModel(client, auth, settings)
		self._responses = None

	def load(self, payload):

		self.requestPool.requests = payload.requestConfig

	def send(self):

		requestor = NonblockRequestor(self.requestPool)

		asyncio.run(requestor.sendPool())

		self._responses = requestor.responses
