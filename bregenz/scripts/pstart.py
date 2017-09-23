"""Module to start application server
"""
from pyramid.paster import (
    get_app,
    setup_logging
)

from bregenz.env import Env


def usage(argv):
    """Prints bregenz_pstart command usage
    """
    import os
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s {development|production}.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv):
    """Start server process
    """
    if len(argv) < 2:
        usage(argv)

    Env.load_dotenv_vars()
    env = Env()

    config_uri = argv[1]
    wsgi_app = get_app(config_uri)
    setup_logging(config_uri)

    from paste.script.cherrypy_server import cpwsgi_server
    cpwsgi_server(wsgi_app, host=env.host, port=env.port,
                  numthreads=10, request_queue_size=100)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv) or 0)
