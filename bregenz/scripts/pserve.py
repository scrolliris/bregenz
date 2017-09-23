"""Module to serve application server
"""
import sys

from pyramid.scripts.pserve import PServeCommand

from bregenz.env import Env


def main(argv=None, quiet=False):
    """Run original pserve with .env support
    """
    if not argv:
        argv = sys.argv

    Env.load_dotenv_vars()

    command = PServeCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main(argv=None, quiet=False) or 0)
