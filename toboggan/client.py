from enum import Enum
from requests import Session
from aiohttp import ClientSession


class ClientType(Enum):

	block = Session()
	nonblock = ClientSession


class SessionProps:

	@property
	def session(self):

		return self._session

	@session.setter
	def session(self, clientType):

		self._session = clientType


class Client(SessionProps):

	_client = None

	def __init__(self, client):

		if client == ClientType.block:

			self.session = ClientType.block.value

		elif client == ClientType.nonblock:

			self.session = ClientType.nonblock.value
