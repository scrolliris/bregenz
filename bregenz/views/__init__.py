"""View action package
"""
from typing import Union


def tpl(path, namespace=None) -> str:
    """Returns template path from package root
    """
    if namespace:
        return 'bregenz:templates/{0:s}/{1:s}'.format(namespace, path)
    else:
        return 'bregenz:templates/{0:s}'.format(path)


def subdomain(request) -> Union[None, str]:
    """Returns subdomain from env DOMAIN via settings
    """
    if request.domain == request.settings.get('domain', None):
        return None

    parts = request.domain.split('.', 2)
    if not len(parts) >= 3:
        return None
    return parts[0]


def includeme(config) -> None:
    """Initializes the view for a bregenz app

    Activate this setup using ``config.include('bregenz.views')``.
    """
    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
