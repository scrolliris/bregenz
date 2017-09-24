"""Module to start application server
"""
import os
import sys

from pyramid.paster import (
    get_app,
    setup_logging
)


def usage(argv):
    """Prints bregenz_pstart command usage
    """
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s {development|production}.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv):
    """Starts main production server process
    """
    if len(argv) < 2:
        usage(argv)

    config_uri = argv[1] if 1 in argv else 'config/production.ini'
    wsgi_app = get_app(config_uri)
    setup_logging(config_uri)

    return wsgi_app


if __name__ == '__main__':
    from paste.script.cherrypy_server import cpwsgi_server
    from bregenz.env import Env

    Env.load_dotenv_vars()
    env = Env()  # pylint: disable=invalid-name
    cpwsgi_server(main(sys.argv), host=env.host, port=env.port,
                  numthreads=10, request_queue_size=100)
