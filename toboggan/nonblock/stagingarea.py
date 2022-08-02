import asyncio
from .nonblockrequestor import NonblockRequestor
from .models import NonblockRequestPoolModel


class StagingArea:

	def __init__(self, client, auth, settings):

		self.requestPool = NonblockRequestPoolModel(client, auth, settings)

	def send(self, requests):

		for request in requests:

			self.requestPool.requests = request

		requestor = NonblockRequestor(self.requestPool)

		asyncio.run(requestor.sendPool())

		return requestor.responses
