"""View action for article
"""
from datetime import datetime
from os import path

# timezone
import sys
import yaml

# pylint: disable=no-name-in-module, ungrouped-imports
if sys.version_info[0] < 3:
    import pytz as timezone
else:
    from datetime import timezone
# pylint: enable=no-name-in-module, ungrouped-imports

# pylint: disable=wrong-import-position
import bleach
import markdown
from pyramid.view import view_config

from bregenz.views import tpl


def render_content(article_path):  # type (str) -> 'function'
    """Return a funciton to parse article content in yaml
    """
    def _content():  # type () -> dict
        if path.isfile(article_path):
            with open(article_path, 'r') as f:
                try:
                    content = yaml.load(f)
                except yaml.YAMLError:
                    content = ''
        else:
            content = ''

        # sanitize
        sanitized_body = bleach.clean(
            content['body'], tags=[], attributes=[],
            styles=[], protocols=[], strip=False, strip_comments=True)
        # convert
        body_html = markdown.markdown(
            sanitized_body, output_format='html5',
            tab_length=2, extensions=[])
        # cleanup
        tags = ['p', 'h3', 'h2', 'h1', 'pre', 'code', 'ul', 'ol', 'li', 'b',
                'i', 'em', 'a', 'br']
        attrs = {'a': ['href'], 'img': ['alt', 'src']}
        content['body'] = bleach.clean(body_html, tags=tags, attributes=attrs)
        return content

    return _content


@view_config(route_name='index',
             renderer=tpl('index.mako'))
def index(_req):
    """Renders a article
    """
    article_path = path.join(
        path.dirname(__file__),
        '../../doc/article/en.yml',
    )
    # create ISO 8601 format string with timezone (+00:00)
    view_date = datetime.now(timezone.utc).isoformat()

    return dict(view_date=view_date,
                render_content=render_content(article_path))
