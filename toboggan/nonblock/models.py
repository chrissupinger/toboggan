from dataclasses import dataclass, field
from typing import Optional, Type
from aiohttp import BasicAuth


@dataclass
class NonblockRequestPool:
	_client: Optional[Type] = field(default=None)
	_auth: Optional[Type] = field(default=None)
	_settings: Optional[dict] = field(default_factory=dict)
	_requests: list[dict] = field(default_factory=list)

	@property
	def client(self):
		return self._client

	@property
	def auth(self):
		return self._auth

	@property
	def settings(self):
		return self._settings

	@property
	def requests(self):
		return self._requests

	@client.setter
	def client(self, clientType):
		self._client = clientType

	@auth.setter
	def auth(self, creds: tuple):
		self._auth = BasicAuth(*creds) if creds else self._auth

	@settings.setter
	def settings(self, fields):
		for key, value in fields.items():
			self._settings[key] = value

	@requests.setter
	def requests(self, request):
		self._requests.append(request)


@dataclass
class NonblockResponse:
	_status_code: Optional[int] = field(default=500)
	_json: Optional[dict] = field(default=dict)

	@property
	def status_code(self):
		return self._status_code

	@property
	def json(self):
		return self._json

	@status_code.setter
	def status_code(self, code):
		self._status_code = code

	@json.setter
	def json(self, data):
		self._json = data


@dataclass
class NonblockResponses:
	_responses: list = field(default_factory=list)

	@property
	def responses(self):
		return self._responses

	@responses.setter
	def responses(self, resp):
		self._responses.append(resp)


@dataclass
class NonblockTasks:
	_tasks: list = field(default_factory=list)

	@property
	def tasks(self):
		return self._tasks

	@tasks.setter
	def tasks(self, task):
		self._tasks.append(task)
