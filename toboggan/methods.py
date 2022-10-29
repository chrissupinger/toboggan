from .blockrequestor import BlockRequestor
from .client import ClientType
from .payload import Payload


class MethodConstructor:

	def __call__(self, func):
		def arg_handler(*args, **kwargs):
			connector = next(iter(args))
			kwargs.update(dict(path=self.path))
			payload = Payload(connector, kwargs, self.method, self.request_settings)
			if self.payload_inspector:
				print(payload)
			if payload.session == ClientType.block:
				return BlockRequestor(payload)
			elif payload.session == ClientType.nonblock:
				return payload.request_config
		return arg_handler


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

	@property
	def request_settings(self):
		return self._request_settings


class MethodTemplate(MethodProps):

	def __init__(self, method, path: str, payload_inspector, **kwargs):
		self._method = method
		self._path = path
		self._payload_inspector = payload_inspector
		self._request_settings = kwargs


class Delete(MethodTemplate, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False, **kwargs):
		super().__init__(
			self.__class__.__name__.upper(), path, payload_inspector, **kwargs)


class Get(MethodTemplate, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False, **kwargs):
		super().__init__(
			self.__class__.__name__.upper(), path, payload_inspector, **kwargs)


class Options(MethodTemplate, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False, **kwargs):
		super().__init__(
			self.__class__.__name__.upper(), path, payload_inspector, **kwargs)


class Post(MethodTemplate, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False, **kwargs):
		super().__init__(
			self.__class__.__name__.upper(), path, payload_inspector, **kwargs)


class Put(MethodTemplate, MethodConstructor):

	def __init__(self, path: str = None, payload_inspector=False, **kwargs):
		super().__init__(
			self.__class__.__name__.upper(), path, payload_inspector, **kwargs)
