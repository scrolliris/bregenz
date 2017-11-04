from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.view import notfound_view_config

from bregenz.views import tpl


@notfound_view_config(renderer=tpl('404.mako'),
                      append_slash=HTTPMovedPermanently)
def notfound(request):
    """Renders not found error view."""
    request.response.status = 404
    return {}
