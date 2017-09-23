from os import path
import json

from bleach import clean as _clean
from markupsafe import Markup

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_template_util_renderer_globals(evt):
    """Adds template utility instance as `util`
    """
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    if util is None and req is not None:
        from bregenz import get_settings

        util = get_settings()['bregenz.includes']['template_util'](ctx, req)
    evt['util'] = util
    evt['clean'] = clean


def clean(**kwargs) -> 'function':
    """Returns sanitized value except allowed tags and attributes

    >>> ${'<a href="/"><em>link</em></a>'|n,clean(
            tags=['a'], attributes=['href'])}
    "<a href="/">link</a>"
    """
    def __clean(text) -> Markup:
        return Markup(_clean(text, **kwargs))

    return __clean


class TemplateUtil(object):
    """The utility for templates
    """
    def __init__(self, ctx, req, **kwargs):
        self.ctx, self.req = ctx, req

        from bregenz.env import Env
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
    def manifest_json(self):
        manifest_file = path.join(
            path.dirname(__file__), '..', '..', 'static', 'manifest.json')
        data = {}
        if path.isfile(manifest_file):
            with open(manifest_file) as data_file:
                data = json.load(data_file)
        return data

    @reify
    def typekit_id(self):
        return self._env.get('TYPEKIT_ID', '')

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

    def static_url(self, path):
        return self.req.static_url('bregenz:../static/' + path)

    def static_path(self, path):
        return self.req.static_path('bregenz:../static/' + path)

    def built_asset_url(self, path):
        path = self.manifest_json.get(path, path)
        return self.static_url(path)
