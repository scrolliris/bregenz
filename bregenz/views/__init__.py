"""View action package
"""
from typing import Union, List

from pyramid.config import Configurator
from pyramid.request import Request


def tpl(path, namespace=None):  # type (str, List[str, None]) -> str
    """Returns template path from package root
    """
    if namespace:
        return 'bregenz:templates/{0:s}/{1:s}'.format(namespace, path)
    else:
        return 'bregenz:templates/{0:s}'.format(path)


def subdomain(request):  # type (Request) -> Union[None, str]
    """Returns subdomain from env DOMAIN via settings
    """
    if request.domain == request.settings.get('domain', None):
        return None

    parts = request.domain.split('.', 2)
    if not len(parts) >= 3:
        return None
    return parts[0]


def includeme(config):  # type (Configurator) -> None
    """Initializes the view for a bregenz app

    Activate this setup using ``config.include('bregenz.views')``.
    """
    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
