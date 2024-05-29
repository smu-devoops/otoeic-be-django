import logging

from . import log_filters


class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class LogUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django')
        if request.user.is_authenticated:
            # 로거에 커스텀 필터 추가
            user_filter = log_filters.RequestUserFilter()
            user_filter.username = request.user.username
            logger.addFilter(user_filter)
        response = self.get_response(request)
        return response
