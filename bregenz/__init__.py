from pyramid.config import Configurator
from pyramid.util import DottedNameResolver
from pyramid.threadlocal import get_current_registry

from bregenz.env import Env


def get_settings():
    """Returns settings from current ini."""
    return get_current_registry().settings


def resolve_settings(settings):
    """Resolving settings."""
    s = settings.copy()
    settings_defaults = {
        'bregenz.includes': {
            'template_util': 'bregenz.utils.template.TemplateUtil',
        }
    }
    for k, v in settings_defaults.items():
        s.setdefault(k, v)

    s = resolve_names(s)
    s = resolve_env_vars(s)
    return s


def resolve_names(settings, directive='bregenz.includes'):
    """Resolves dotted module names."""
    s = settings.copy()
    for k, v in s[directive].items():
        if not isinstance(v, str):
            continue
        s[directive][k] = DottedNameResolver().resolve(v)
    return s


def resolve_env_vars(settings):
    """Returns settings resolved with vars from os.environ."""
    def get_new_v(env, value, expected_type):
        """Gets expected value from environ variable."""
        new_v = env.get(value, None)
        if not isinstance(new_v, expected_type):
            return None
        # split, but ignore empty string
        if ',' in new_v:
            new_v = [v for v in new_v.split(',') if v != '']
        return new_v

    env = Env()
    s = settings.copy()
    for k, v in Env.settings_mappings().items():
        # ignores missing key or it has a already value in config
        if k not in s or s[k]:
            continue
        new_v = get_new_v(env, v, str)
        if new_v:
            s[k] = new_v
    return s


def main(_global_config, **settings):
    from bregenz.request import CustomRequest

    config = Configurator(settings=resolve_settings(dict(settings)))

    config.add_tween('.tweens.ssl_suggestion.tween_factory')

    config.include('.route')
    config.include('.views')

    # this calls db connect/close to recycle connection
    config.set_request_factory(CustomRequest)

    config.set_default_csrf_options(require_csrf=True)
    config.scan()

    app = config.make_wsgi_app()
    # enable file logger [wsgi/access_log]
    # from paste.translogger import TransLogger
    # app = TransLogger(app, setup_console_handler=False)

    # basic auth
    env = Env()
    credentials = settings.get('wsgi.auth_credentials', None)
    if not env.is_test and credentials and credentials != '':
        env.set('WSGI_AUTH_CREDENTIALS', credentials)
        from wsgi_basic_auth import BasicAuth
        app = BasicAuth(app)
    return app
