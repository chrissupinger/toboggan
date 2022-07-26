# toboggan

Most def inspired by [prkumar's](https://github.com/prkumar) work on [Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  The plan is to eventually implement support for nonblocking requests created with [aiohttp](https://github.com/aio-libs/aiohttp).

## Usage w/ [httpbin](https://github.com/postmanlabs/httpbin)

### Your class

``` python
from toboggan import Connector, Get, Headers


@Headers({'Content-Type': 'application/json'})
class Httpbin(Connector):

	def __init__(self):

		super().__init__(
			base='https://httpbin.org'
		)

	@Get(path='ip')
	def ip(self):

		pass
```

### Your instantiation

``` python
httpbin = Httpbin()
```

### Your invocation

``` python
myIp = httpbin.ip()
```

### Your response

``` python
print(myIp.json)

# {'origin': '<YOUR_IP_ADDRESS>'}
```