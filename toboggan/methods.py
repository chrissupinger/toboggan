from .payload import Payload
from .requestor import Requestor


class MethodConstructor:

	def __call__(self, func):

		def argHandler(*args, **kwargs):

			kwargs.update(dict(path=self.path))

			payload = Payload(next(iter(args)), kwargs, self.method)

			return Requestor(payload, self.payload_inspector)

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
