from .client import Client, ClientType
from .nonblock.stagingarea import StagingArea


class ConnectorProps:

	@property
	def client(self):

		return self._client

	@property
	def base(self):

		return self._base

	@property
	def headers(self):

		return self._headers

	@property
	def auth(self):

		return self._auth

	@property
	def settings(self):

		return self._kwargs

	@property
	def staging(self):

		return self._staging

	@client.setter
	def client(self, client):

		self._client = client

	@headers.setter
	def headers(self, fields):

		for key, value in fields.items():

			self._headers[key] = value


class Connector(ConnectorProps):
	"""Represents the constructor that manages the session and its base properties.
	"""

	def __init__(self, base: str, auth=None, client=ClientType.block, **kwargs) -> None:

		self._client = Client(client).session
		self._base = base
		self._headers = dict()
		self._auth = auth
		self._kwargs = kwargs

		if client == ClientType.nonblock:

			self._staging = StagingArea(self.client, self.auth, self.settings)
