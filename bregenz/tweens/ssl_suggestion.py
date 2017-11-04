import logging

from bregenz.utils.localization import get_translator_function


def config_get(registry):
    s = registry.settings

    def _get_config(key, default):
        v = str(s.get('ssl_suggestion.{}'.format(key), default))
        if v.lower() == 'true':
            return True
        elif v.lower() == 'false':
            return False

        return v

    return _get_config


def set_flash_message(req, key='ssl.suggestion.message', queue='announcement'):
    _ = get_translator_function(req.localizer)
    req.session.flash(_(key), queue=queue, allow_duplicate=False)
    return req


def set_hsts_header(res):
    # Sets HSTS Policy
    # about preload, see https://hstspreload.org/
    # see details below:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/\
    #   Strict-Transport-Security#Preloading_Strict_Transport_Security
    age = 31536000  # seconds (one year)
    hsts_policy = 'max-age={0}; includeSubDomains'.format(age)
    res.headers['Strict-Transport-Security'] = hsts_policy
    return res


def tween_factory(handler, registry):
    """Suggests new url with ssl via flash message."""
    get_config = config_get(registry)

    hsts_header = get_config('hsts_header', 'False')
    flash_message = get_config('flash_message', 'False')
    proto_header = get_config('proto_header', None)

    def ssl_suggestion_tween(req):
        """Handles request with ssl checker and suggestions."""
        criteria = [
            req.url.startswith('https://'),
            (not req.path.startswith('/assets/')),
        ]
        if proto_header:
            criteria.append(
                req.headers.get(proto_header, 'http') == 'https')

        if all(criteria) or not (hsts_header or flash_message):
            return handler(req)
        else:
            if flash_message:
                req = set_flash_message(req)

            res = handler(req)

            if hsts_header:
                res = set_hsts_header(res)

            logger = logging.getLogger(__name__)
            logger.info('[INSECURE] requst.url: %s', req.url)

            return res

    return ssl_suggestion_tween
