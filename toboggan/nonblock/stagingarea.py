import asyncio
from .nonblockrequestor import NonblockRequestor
from .models import NonblockRequestPool


class StagingArea:

	def __init__(self, client, auth, settings):
		self.request_pool = NonblockRequestPool(client, auth, settings)

	def send(self, requests):
		for request in requests:
			self.request_pool.requests = request
		requestor = NonblockRequestor(self.request_pool)
		asyncio.run(requestor.send_pool())
		return requestor.responses
