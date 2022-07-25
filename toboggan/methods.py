from .payload import Payload
from .requestor import Requestor


class MethodConstructor:

	def __call__(self, func):

		def argHandler(*args, **kwargs):

			kwargs.update(dict(path=self.path))

			payload = Payload(
				connector=next(iter(args)),
				request=kwargs,
				method=self.method,
			)

			return Requestor(payload)

		return argHandler


class MethodProps:

	@property
	def method(self):

		return self._method

	@property
	def path(self):

		return self._path


class Delete(MethodProps, MethodConstructor):

	def __init__(self, path: str = None):

		self._method = self.__class__.__name__.upper()
		self._path = path


class Get(MethodProps, MethodConstructor):

	def __init__(self, path: str = None):

		self._method = self.__class__.__name__.upper()
		self._path = path


class Options(MethodProps, MethodConstructor):

	def __init__(self, path: str = None):

		self._method = self.__class__.__name__.upper()
		self._path = path


class Post(MethodProps, MethodConstructor):

	def __init__(self, path: str = None):

		self._method = self.__class__.__name__.upper()
		self._path = path


class Put(MethodProps, MethodConstructor):

	def __init__(self, path: str = None):

		self._method = self.__class__.__name__.upper()
		self._path = path
