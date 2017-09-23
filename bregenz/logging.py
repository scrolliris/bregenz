import logging
from pyramid.events import ContextFound
from pyramid.events import subscriber


@subscriber(ContextFound)
def context_found(event):
    request = event.request
    # quiet access to assets
    if not getattr(request, 'path', '').startswith('/assets'):
        logger = logging.getLogger(__name__)
        route = getattr(request, 'matched_route', None)
        logger.info('{0:s} {1:d} {2:s} {3:s} {4:s} {5:s}'.format(
            request.method,
            request.response.status_code,
            request.path_qs,
            route.name if route else '',
            str(request.matchdict),
            str(request.params)))
