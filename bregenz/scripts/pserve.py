import sys

from bregenz.env import Env


def main(argv=None, quiet=False):
    # `pserve` (PServeCommand) needs `hupper`, `hupper` has dependency
    # **fcntl**. In some environment (e.g. app engine), fcntl is not found :'(
    from pyramid.scripts.pserve import PServeCommand

    if not argv:
        argv = sys.argv

    Env.load_dotenv_vars()

    command = PServeCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main(argv=None, quiet=False) or 0)
