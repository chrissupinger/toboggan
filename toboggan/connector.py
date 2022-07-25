from requests import Session


class ConnectorProps:

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
	def blockSettings(self):

		return dict(
			timeout=self._kwargs.get('timeout'),
			proxies=self._kwargs.get('proxies'),
			verify=self._kwargs.get('verify', True),
			stream=self._kwargs.get('stream'),
			cert=self._kwargs.get('cert')
		)

	@headers.setter
	def headers(self, fields):

		for key, value in fields.items():

			self._headers[key] = value


class Client:

	def __init__(self, client):

		self._client = client

	@property
	def client(self):

		return self._client

	@client.setter
	def client(self, client):

		self._client = client


class Connector(ConnectorProps, Client):
	"""Represents the constructor that manages the session and its base properties.
	"""

	def __init__(self, base: str, auth=None, client: Session = Session(), **kwargs) -> None:

		super().__init__(client=client)

		self._base = base
		self._headers = dict()
		self._auth = auth
		self._kwargs = kwargs
