import logging

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.log import ServerFormatter


class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request: HttpRequest):
        response: HttpResponse = self.get_response(request)
        req_msg = "{method} {path} {protocol}".format(
            method = request.method,
            path = request.path,
            protocol = request.environ.get('SERVER_PROTOCOL'),
        )
        res_msg = "{status}".format(
            status = response.status_code
        )
        usr_msg = "[{user}@{host}]".format(
            user = request.user,
            host = request.get_host(),
        )
        logger = logging.getLogger('django')
        logger.log(logging.INFO, f"[Summary] \"{req_msg}\" {res_msg} {usr_msg}")
        return response
