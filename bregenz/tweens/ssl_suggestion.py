import ast
import logging

from bregenz.utils.localization import get_translator_function


def tween_factory(handler, registry):
    """This tween suggests does not redirect by itself, suggests new url with
    ssl via flash message instead
    """
    s = registry.settings
    ssl_suggestion = ast.literal_eval(s.get('ssl_suggestion', 'False'))

    def ssl_suggestion_tween(request):
        criteria = [
            request.headers.get('X-FORWARDED-PROTO', 'http') == 'https',
            request.url.startswith('https://'),
        ]
        if all(criteria) or not ssl_suggestion:
            return handler(request)
        else:
            request_to_assets = request.path.startswith('/assets/')
            if not request_to_assets:
                _ = get_translator_function(request.localizer)
                request.session.flash(_('ssl.suggestion.message'),
                                      queue='announcement',
                                      allow_duplicate=False)

            response = handler(request)

            # Sets HSTS Policy
            # about preload, see https://hstspreload.org/
            # see details below:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/\
            #   Strict-Transport-Security#Preloading_Strict_Transport_Security
            age = 31536000  # seconds (one year)
            hsts_policy = 'max-age={0}; includeSubDomains'.format(age)
            response.headers['Strict-Transport-Security'] = hsts_policy

            if not request_to_assets:
                logger = logging.getLogger(__name__)
                logger.info('[INSECURE] requst.url: %s', request.url)
            return response
    return ssl_suggestion_tween
