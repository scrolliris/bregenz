from typing import Union, List  # noqa

from pyramid.config import Configurator  # noqa
from pyramid.request import Request  # noqa


def tpl(path, namespace=None):  # type (str, List[str, None]) -> str
    if namespace:
        return 'willisau:templates/{0:s}/{1:s}'.format(namespace, path)
    return 'willisau:templates/{0:s}'.format(path)


def subdomain(request):  # type (Request) -> Union[None, str]
    """Returns subdomain from env DOMAIN via settings."""
    if request.domain == request.settings.get('domain', None):
        return None

    parts = request.domain.split('.', 2)
    if not len(parts) >= 3:
        return None
    return parts[0]


def includeme(config):  # type (Configurator) -> None
    """Initializes the view for a willisau app.

    Activate this setup using ``config.include('willisau.views')``.
    """
    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
