from path_dispatcher import PathDispatcher
import time


def add(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ["params"]
    delay = params.get("delay", None)
    name = params.get("name", None)
    print(params)
    print("Waiting ".format(delay))
    yield _resp.encode('utf-8')


_resp = '''\
<html>
  <head>
    <title>{serial}</title>
  </head>
  <body>
    <p>{serial}</p>
  </body>
</html>'''


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/add', add)

    httpd = make_server('', 8080, dispatcher)
    print("Server is working on port 8080..")
    httpd.serve_forever()
