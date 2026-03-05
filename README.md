# toboggan

Inspired by [prkumar's](https://github.com/prkumar) work on 
[Uplink](https://github.com/prkumar/uplink).

toboggan wraps the popular [Requests](https://github.com/psf/requests) library.  There's 
support for nonblocking requests with [aiohttp](https://github.com/aio-libs/aiohttp).

## Table of contents

- [Installation](#installation)
- [Connector](#connector)
- [Client](#client)
- [Decorators](#decorators)
  - [Verbs](#verbs)
  - [headers](#headers)
  - [params](#params)
  - [retry](#retry)
  - [returns.*](#returns)
  - [sends.*](#sends)
- [Annotations](#annotations)
- [Usage](#usage)
  - [Blocking](#blocking-w-httpbin)
  - [Nonblocking](#nonblocking-w-pokéapi)

### Installation

Recommended installation that fits most use cases:

```bash
pip install toboggan
```

For async support w/ aiohttp:

```bash
pip install toboggan[aiohttp]
```

### Connector

The `Connector` class is the base configuration for creating all API models.  It 
can grant any instance method access to a common client session and a wide 
array of settings.  Instantiation can be achieved in various ways:

- Initialization of the inherited superclass in the class's constructor

```python
from toboggan import Connector


class Httpbin(Connector):

    def __init__(self):
        super().__init__(base_url='https://httpbin.org')


httpbin = Httpbin()
```

- Directly calling the class constructor with arguments

```python
from toboggan import Connector


class Httpbin(Connector):
    pass


httpbin = Httpbin(base_url='https://httpbin.org')
```

The `Connector` class is built for reusability.  Even after initial 
instantiation, the `Connector` can be re-instantiated with new `base_url` and 
`client` arguments.  A use case for this is reusing a model in which both 
blocking and nonblocking behavior is desired from mutual or exclusive paths.

```python
from aiohttp import ClientSession
from requests import Session
from toboggan import AiohttpClient, Connector, RequestsClient


class Httpbin(Connector):
    pass


api = Httpbin(base_url='https://httpbin.org', client=Session())
nonblocking = api(base_url='https://httpbin.org', client=ClientSession())
```

### Client

The default client associated to the `Connector` class is `requests.Session`.  For 
nonblocking requests, `aiohttp.ClientSession` can be used.  Changing the client 
type can be achieved through:

- Passing `aiohttp.ClientSession` as a constructor argument

```python
from aiohttp import ClientSession
from toboggan import Connector


class Httpbin(Connector):
    pass


httpbin = Httpbin(base_url='https://httpbin.org', client=ClientSession())
```

- Setting the client via the `Connector.client` setter

```python
from aiohttp import ClientSession
from requests import Session
from toboggan import AiohttpClient, Connector, RequestsClient


class Httpbin(Connector):
    pass


httpbin = Httpbin(base_url='https://httpbin.org', client=ClientSession())
httpbin.client = Session()
```

### Decorators

Decorators are used to statically describe your API models.

#### Verbs

The verb decorators are foundational for your instance methods to use the 
`Connector` and should be applied as the first decorator in a chain.  A verb 
decorator is the minimum requirement for instance methods using the 
`Connector`.  The following HTTP verbs are available for use:

- `connect`
- `delete`
- `get`
- `head`
- `options`
- `patch`
- `post`
- `put`
- `trace`

```python
from toboggan import Connector, get


class Httpbin(Connector):
    
    @get(path='/get')
    def get_(self):
        pass
```

#### headers

The `headers` decorator is versatile and can be employed at both the 
class-level and its instance methods.  When decorating the subclass of the 
`Connector` class, `headers` will designate global values to be applied to 
every instance method that uses the `Connector`.  When decorating an instance 
method, those values are exclusive to the method.

```python
from toboggan import Connector, get, headers


@headers({'Content-Type': 'application/json'})
class Httpbin(Connector):

    @headers({'User-Agent': 'toboggan (python-requests/2.32.3)'})
    @get(path='/get')
    def get_request(self):
        pass
```

#### params

Just like the `headers` decorator, the `params` decorator is versatile.  The 
`params` decorator requires a mapping

```python
from toboggan import Connector, get, params


@params({'limit': 50})
class Httpbin(Connector):

    @params({'email': 'johndoe@example.com'})
    @get(path='/get')
    def get_request(self):
        pass
```

#### retry

The `retry` deocorator sets a retry strategy for requests.  This allows for 
setting a retry count (`total`), an exponential time between retries 
(`backoff_factor`) and conditions for a retry to occur (`status_forcelist`).

```python
from toboggan import Connector, get, retry


class Httpbin(Connector):

    @retry(total=10, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
    @get(path='/get')
    def get_json(self):
        pass
```

#### returns.*

The `returns` decorator grants access to return types that can be used to 
preemptively declare an expected return type.  When the decorated instance 
method is invoked, the designated return type will be loaded.  If no return 
type is designated, a client respective response object is returned.  The 
following return types are available for use:

- `json`
- `status_code`
- `text`

```python
from toboggan import Connector, get, returns


class Httpbin(Connector):

    @returns.json
    @get(path='/get')
    def get_json(self):
        pass
    
    @returns.status_code
    @get(path='/get')
    def get_status_code(self):
        pass
    
    @returns.text
    @get(path='/get')
    def get_text(self):
        pass
```

The `json` return type is able to take a `key` argument.  This argument allows 
the method to return a nested key-value pair.  If `key` is not set, the entire 
JSON object is returned from the response.  Both `status_code` and `text` do 
not take arguments.

```python
from toboggan import Connector, get, returns


class Httpbin(Connector):

    @returns.json(key='json')
    @get(path='/get')
    def get_json(self):
        pass
```

#### sends.*

The `sends` decorator grants access to data send types that can be used to 
preemptively declare a data send type.  When the decorated instance method is 
invoked, the designated data send type will be configured for the request.  If 
no data send type is designated, a data send type will be coerced based on 
the data type passed to the `Body` of the request.

- `form_url_encoded`
- `json`

```python
from toboggan import Body, Connector, post, sends


class Httpbin(Connector):

    @sends.form_url_encoded
    @post(path='/post')
    def post_data(self, body: Body):
        pass
    
    @sends.json
    @post(path='/post')
    def post_json(self, body: Body):
        pass
```

The `form_url_encoded` data send type configures a request to send form-encoded 
data.  The `json` data send type configures the request to send JSON-encoded 
data.  Both `form_url_encoded` and `json` do not take arguments.

### Annotations

Annotations are used to designate dynamic values that your models will consume.  These 
are employed as type hints for instance method arguments.  The following 
annotations are available for use:

- `Body`
- `Options`
- `Path`
- `Query`
- `QueryKebab`

```python
from toboggan import Body, Connector, Path, Query, QueryKebab, get, post


class Httpbin(Connector):
    
    @post(path='/post')
    def post_w_body(self, body: Body):
        pass
    
    @get(path='/anything/{path_param}')
    def get_w_path_param(self, path_param: Path):
        pass
    
    @get(path='/get')
    def get_w_query_params(self, limit: Query, page_size: QueryKebab):
        pass

    @get(path='/get')
    def get_w_options(self, **options: Options):
        pass
```

The `Body` type annotates the body of the request.  The `Path` type annotates a 
request path parameter.  The `Query` type annotates a request query parameter.  A 
single method can only have one `Body` annotation and an unlimited number of 
`Path` and `Query` annotations.

The `QueryKebab` type is an extenstion of the `Query` type.  This is used for 
APIs that still employ kebab casing for their query parameters.  When assigned 
these types, parameters should be delimited by an underscore (`_`) or, in other 
words, snake cased.  This annotation coerces snake case to kebab case.

The `Options` type allows arbitrary keyword arguments to be declared for a 
method.  When using the `Options` annotation, arguments should reflect a client 
type's request keyword arguments.  For `Requests`, 
see: [requests.Session.request](https://docs.python-requests.org/en/latest/api/#requests.Session.request).  For
`aiohttp`, see: [aiohttp.ClientSession.request](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request).

### Usage

#### Blocking w/ [httpbin](https://github.com/postmanlabs/httpbin)

```python
from toboggan import Body, Connector, get, headers, post


@headers({'Content-Type': 'application/json'})
class Httpbin(Connector):
    """A httpbin mapping.

    This example and mapping is facilitated with the Docker image.  To 
    run it locally, see usage below.

    If wanting to use the hosted httpbin service, set the `base_url` to
    https://httpbin.org.

    ::

        docker pull kennethreitz/httpbin
        docker run -p 80:80 kennethreitz/httpbin

    References:
        - `httpbin hosted <https://httpbin.org/>`_
        - `httpbin on GitHub <https://github.com/postmanlabs/httpbin>`_
    """

    @get(path='/get')
    def get_request(self):
        """The request's query parameters.
        """

    @post(path='/post')
    def post_request(self, body: Body):
        """The request's POST parameters.
        """


if __name__ == '__main__':
    httpbin = Httpbin(base_url='http://0.0.0.0')

    response = httpbin.get_request()

    request_body = {
        "user_id": 12345,
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "Hello, world!",
        "tags": ["general", "greeting"],
        "data": {
            "age": 30,
            "city": "New York"
        }
    }
    response = httpbin.post_request(body=request_body)
```

#### Nonblocking w/ [PokéAPI](https://pokeapi.co/)

```python
import asyncio
from aiohttp import ClientSession
from toboggan import Connector, Path, get, headers, returns


@headers({'Content-Type': 'application/json'})
class PokeApi(Connector):
    """A PokéAPI mapping.

    References:
        - `PokéAPI <https://pokeapi.co>`_
    """

    @returns.json(key=('species', 'name',))
    @get('pokemon/{no}')
    def get_pokemon(self, no: Path) -> str:
        """Retrieve Pokémon metadata.  Traverse the nested dictionary 
        returned and get the `name` value.

        References:
            - `Pokémon (endpoint) <https://pokeapi.co/docs/v2#pokemon>`_
        """


if __name__ == '__main__':
    # Utilizing `asyncio.run` for Python 3.7 and above.
    async def poke_api_async(range_):
        poke_api = PokeApi(
            base_url='https://pokeapi.co/api/v2/', client=ClientSession()
        )
        async with poke_api.session():
            tasks = [poke_api.get_pokemon(no=no) for no in range_]
            responses = await gather(*tasks)
            return responses

    responses = asyncio.run(poke_api_async(range_=range(1, 152)))

    # For < 3.7, use an event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(poke_api_async(range_=range(1, 152)))
```