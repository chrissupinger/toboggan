from .blockrequestor import BlockRequestor
from .client import ClientType
from .payload import Payload


class MethodConstructor:

	def __call__(self, func):

		def argHandler(*args, **kwargs):

			connector = next(iter(args))

			kwargs.update(dict(path=self.path))

			payload = Payload(connector, kwargs, self.method)

			if payload.session == ClientType.block.value:

				return BlockRequestor(payload, self.payload_inspector)

			elif payload.session == ClientType.nonblock.value:

				return payload.requestConfig

		return argHandler


class MethodProps:

	@property
	def method(self):

		return self._method

	@property
	def path(self):

		return self._path

	@property
	def payload_inspector(self):

		return self._payload_inspector


class Delete(MethodProps, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False):

		self._method = self.__class__.__name__.upper()
		self._path = path
		self._payload_inspector = payload_inspector


class Get(MethodProps, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False):

		self._method = self.__class__.__name__.upper()
		self._path = path
		self._payload_inspector = payload_inspector


class Options(MethodProps, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False):

		self._method = self.__class__.__name__.upper()
		self._path = path
		self._payload_inspector = payload_inspector


class Post(MethodProps, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False):

		self._method = self.__class__.__name__.upper()
		self._path = path
		self._payload_inspector = payload_inspector


class Put(MethodProps, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False):

		self._method = self.__class__.__name__.upper()
		self._path = path
		self._payload_inspector = payload_inspector
