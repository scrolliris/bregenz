from os import path
import json
import re

from bleach import clean as _clean
from markupsafe import Markup

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender

UNSLASH_PATTERN = re.compile(r'^\/|\/$')


@subscriber(BeforeRender)
def add_template_util_renderer_globals(evt):
    """Adds template utility instance as `util`."""
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    if util is None and req is not None:
        from willisau import get_settings

        util = get_settings()['willisau.includes']['template_util'](ctx, req)
    evt['util'] = util
    evt['clean'] = clean


def clean(**kwargs):  # type (dict) -> 'function'
    """Returns sanitized value except allowed tags and attributes.

    The usage looks like:

    ```
    ${'<a href="/"><i>link</i></a>'|n,clean(tags=['a'], attributes=['href'])}
    ```

    >>> from willisau.utils.template import clean

    >>> type(clean(tags=['a'], attributes=['href']))
    <class 'function'>

    >>> c = clean(tags=['a'], attributes=['href'])
    >>> str(c('<a href="/"><em>link</em></a>'))
    '<a href="/">&lt;em&gt;link&lt;/em&gt;</a>'
    """
    def __clean(text):  # type (str) -> Markup
        return Markup(_clean(text, **kwargs))

    return __clean


class TemplateUtil(object):
    def __init__(self, ctx, req, **kwargs):
        self.ctx, self.req = ctx, req

        from willisau.env import Env
        self._env = Env()

        if getattr(req, 'util', None) is None:
            req.util = self
        self.__dict__.update(kwargs)

    @reify
    def route_name(self):
        route = self.req.matched_route
        if route:
            return route.name

    @reify
    def manifest_json(self):  # pylint: disable=no-self-use
        manifest_file = path.join(
            path.dirname(__file__), '..', '..', 'static', 'manifest.json')
        data = {}
        if path.isfile(manifest_file):
            with open(manifest_file) as data_file:
                data = json.load(data_file)
        return data

    @reify
    def scrolliris_project_id(self):
        return self._env.get('SCROLLIRIS_PROJECT_ID', '')

    @reify
    def scrolliris_read_key(self):
        return self._env.get('SCROLLIRIS_READ_KEY', '')

    @reify
    def scrolliris_write_key(self):
        return self._env.get('SCROLLIRIS_WRITE_KEY', '')

    @reify
    def is_production(self):
        return not self._env.is_production

    @reify
    def cache_article(self):
        return str(self._env.get('CACHE_ARTICLE', 'false')).lower() == 'true'

    def is_matched(self, matchdict):
        return self.req.matchdict == matchdict

    def static_url(self, filepath):  # type: (str) -> str
        from willisau.route import STATIC_DIR

        def get_bucket_info(name):
            part = self.req.settings.get('storage.bucket_{0:s}'.format(name))
            if not part:
                # returns invalid path
                return ''
            return re.sub(UNSLASH_PATTERN, '', part)

        if self._env.is_production:
            h, n, p = [get_bucket_info(x) for x in ('host', 'name', 'path')]
            return 'https://{0:s}/{1:s}/{2:s}/{3:s}'.format(h, n, p, filepath)
        return self.req.static_url(STATIC_DIR + '/' + filepath)

    def static_path(self, filepath):
        from willisau.route import STATIC_DIR

        return self.req.static_path(STATIC_DIR + '/' + filepath)

    def hashed_asset_url(self, filepath):
        return self.static_url(self.manifest_json.get(filepath, filepath))
