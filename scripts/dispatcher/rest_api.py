from path_dispatcher import PathDispatcher
import os


MARS_PATH = "/tmp/cs/risk/app/mars"
RELEASES_PATH = os.path.join(MARS_PATH, "releases")
THIRD_PARTY_VERSION = os.path.join(MARS_PATH, ".3rd_party_version")
THIRD_PARTY_SCRIPTS_VERSION = os.path.join(MARS_PATH, ".3rd_party_scripts_version")
BIN_VERSION_FILE = ".bin_version"
CFG_VERSION_FILE = ".cfg_version"


def get_version(file_path):
    with open(file_path) as f:
        version = f.read()
    return version


_third_party_resp = '''\
<html>
  <head>
    <title>{host}</title>
  </head>
  <body>
    <p>{name}: {version}</p>
  </body>
</html>'''


def third_party_version(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    host = environ['HTTP_HOST'].split(":")[0]

    version = get_version(THIRD_PARTY_VERSION)
    resp = _third_party_resp.format(host=host, name="third_party_version", version=version)
    yield resp.encode('utf-8')


def third_party_scripts_version(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    host = environ['HTTP_HOST'].split(":")[0]

    version = get_version(THIRD_PARTY_SCRIPTS_VERSION)
    resp = _third_party_resp.format(host=host, name="third_party_scripts_version", version=version)
    yield resp.encode('utf-8')


_env_resp = '''\
<html>
  <head>
    <title>{host}</title>
  </head>
  <body>
    {body}
  </body>
</html>'''


_env_version="<p>  {env}: major version: {dir}, bin: {bin_version}, cfg: {cfg_version}</p>\n"
_separator="<p>" + 100 * "-" + "</p>\n"


def env_version(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    host = environ['HTTP_HOST'].split(":")[0]

    params = environ['params']
    env = params.get('env')
    version = params.get('version')

    envs = [env] if env else os.listdir(RELEASES_PATH)
    body = ""
    for env in envs:
        env_path = os.path.join(RELEASES_PATH, env)
        dirs = [version] if version else os.listdir(env_path)
        for dir in dirs:
            bin_version = get_version(os.path.join(env_path, dir, BIN_VERSION_FILE))
            cfg_version = get_version(os.path.join(env_path, dir, CFG_VERSION_FILE))
            body += _env_version.format(env=env, dir=dir, bin_version=bin_version, cfg_version=cfg_version)
        body += _separator

    resp = _env_resp.format(host=host, body=body)
    yield resp.encode('utf-8')


_hello_resp = '''\
<html>
  <head>
    <title>Hello, {name}</title>
  </head>
  <body>
    <h1>Hello, {name}</h1>
    heheheheheheheh
  </body>
</html>'''


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/third_party_version', third_party_version)
    dispatcher.register('GET', '/third_party_scripts_version', third_party_scripts_version)
    dispatcher.register('GET', '/env_version', env_version)

    httpd = make_server('', 8080, dispatcher)
    print("Server is working on port 8080..")
    httpd.serve_forever()
