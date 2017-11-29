from contextlib import contextmanager
from os import path

from .env import Env


class SubdomainPredicate(object):
    def __init__(self, val, _config):
        self.val = val

    def text(self):
        return 'subdomain = %s' % str(self.val)

    phash = text

    def __call__(self, context, request):
        subdomain = request.subdomain
        if subdomain is None:
            subdomain = 'try'
        return str(subdomain) == self.val


def subdomain_pregenerator(subdomain):
    env = Env()

    def pregenerator(_request, elements, kw):
        domain = env.get('DOMAIN_APPLICATION', None)
        if subdomain:
            kw['_host'] = '{0!s}.{1!s}'.format(subdomain, domain)
        else:
            kw['_host'] = '{0!s}'.format(domain)
        return elements, kw
    return pregenerator


def subdomain_manager(config):
    @contextmanager
    def subdomain(subdomain=None):
        if subdomain is None:
            subdomain = ''
        pregenerator = subdomain_pregenerator(subdomain)

        original_add_route = config.__class__.add_route

        def add_route(self, *args, **kw):
            kw['subdomain'] = subdomain
            kw['pregenerator'] = pregenerator
            original_add_route(self, *args, **kw)

        try:
            import types
            config.add_route = types.MethodType(add_route, config)
            yield config
        finally:
            config.add_route = types.MethodType(original_add_route, config)

    return subdomain


def subdomain_manager_factory(config):
    config.add_route_predicate('subdomain', SubdomainPredicate)
    return subdomain_manager(config)


def includeme(config):
    env = Env()

    # see also __init__.py for static files
    cache_max_age = 3600 if env.is_production else 0

    # static files at /*
    static_dir = path.join(path.dirname(path.abspath(__file__)), '../static')
    filenames = [f for f in ('robots.txt', 'humans.txt', 'favicon.ico')
                 if path.isfile((static_dir + '/{}').format(f))]
    config.add_asset_views(
        'willisau:../static', filenames=filenames, http_cache=cache_max_age)

    # static files at /assets/*
    config.add_static_view(
        name='assets', path='willisau:../static/', cache_max_age=cache_max_age)

    subdomain = subdomain_manager_factory(config)

    # try.example.org, example.org
    with subdomain('try') as c:
        c.add_route('index', '/')
