from json import dumps
from toboggan import (
    Body, Connector, RequestsClient, ResponseObject, get, headers, post,)


@headers({'Content-Type': 'application/json'})
class Httpbin(Connector):
    """A httpbin mapping.

    This example and mapping is facilitated with the Docker image.  To run it
    locally, see usage below.

    If wanting to use the hosted httpbin service, set the `base_url` to
    https://httpbin.org.

    ::

        docker pull kennethreitz/httpbin
        docker run -p 80:80 kennethreitz/httpbin

    References:
        - `httpbin hosted <https://httpbin.org/>`_
        - `httpbin on GitHub <https://github.com/postmanlabs/httpbin>`_
    """

    def __init__(self):
        super().__init__(base_url='http://0.0.0.0', client=RequestsClient())

    @get(path='/get')
    def get_(self) -> ResponseObject:
        """The request's query parameters.
        """

    @post(path='/post')
    def post_(self, body: Body) -> ResponseObject:
        """The request's POST parameters.
        """


if __name__ == '__main__':
    httpbin = Httpbin()

    response = httpbin.get_()
    print(dumps(response.json(), indent=4, default=str))

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
    response = httpbin.post_(body=request_body)
    print(dumps(response.json(), indent=4, default=str))
