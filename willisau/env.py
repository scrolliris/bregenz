from __future__ import print_function
import os

# pylint: disable=wrong-import-position
from pyramid.decorator import reify


# OS's environ handler (wrapper)
# This class has utilities to treat environment variables.
class Env(object):
    VALUES = ('development', 'test', 'production')

    def __init__(self):
        self._value = self.__class__.env_name()

    @classmethod
    def env_name(cls):
        v = str(os.environ.get('ENV', None))
        return v if v in cls.VALUES else 'production'

    @classmethod
    def load_dotenv_vars(cls, dotenv_file=None):
        # loads .env
        if dotenv_file is None:
            dotenv_file = os.path.join(os.getcwd(), '.env')
        if os.path.isfile(dotenv_file):
            print('loading environment variables from .env')
            from dotenv import load_dotenv
            load_dotenv(dotenv_file)

        # update vars using prefix such as {TEST_|DEVELOPMENT_|PRODUCTION_}
        for _, v in cls.settings_mappings().items():
            prefix = '{}_'.format(cls.env_name().upper())
            env_v = os.environ.get(prefix + v, None)
            if env_v is not None:
                os.environ[v] = env_v

    @staticmethod
    def settings_mappings():  # type () -> dict
        return {
            # Note: these values are updated if exist but not empty
            'domain': 'DOMAIN',
            'session.type': 'SESSION_TYPE',
            'session.secret': 'SESSION_SECRET',
            'session.key': 'SESSION_KEY',
            'session.url': 'SESSION_URL',
            'session.username': 'SESSION_USERNAME',
            'session.password': 'SESSION_PASSWORD',
            'session.cookie_domain': 'SESSION_COOKIE_DOMAIN',
            'ssl_suggestion.flash_message': 'SSL_SUGGESTION_FLASH_MESSAGE',
            'ssl_suggestion.hsts_header': 'SSL_SUGGESTION_HSTS_HEADER',
            'ssl_suggestion.proto_header': 'SSL_SUGGESTION_PROTO_HEADER',
            'bucket.host': 'BUCKET_HOST',
            'bucket.name': 'BUCKET_NAME',
            'bucket.path': 'BUCKET_PATH',
            'wsgi.url_scheme': 'WSGI_URL_SCHEME',
            'wsgi.auth_credentials': 'WSGI_AUTH_CREDENTIALS',
        }

    def get(self, key, default=None):  # pylint: disable=no-self-use
        return os.environ.get(key, default)

    def set(self, key, value):  # pylint: disable=no-self-use
        os.environ[key] = value

    @reify
    def host(self):
        # TODO:
        # get host and port from server section in ini as fallback
        return str(self.get('HOST', '127.0.0.1'))

    @reify
    def port(self):
        return int(self.get('PORT', 5000))

    @reify
    def value(self):
        return self._value

    @reify
    def is_test(self):
        return self._value == 'test'

    @reify
    def is_production(self):
        return self._value == 'production'
