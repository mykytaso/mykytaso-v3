import logging
import time

from utils.request import get_client_ip


log = logging.getLogger("request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        domain = request.get_host()
        requester_ip = get_client_ip(request)
        status_code = response.status_code
        method = request.method
        path = request.path
        referer = request.META.get("HTTP_REFERER", "-")
        user_agent = request.META.get("HTTP_USER_AGENT", "-")

        if "uptimerobot" in user_agent:
            log.info("Uptime Robot check")
        else:
            log.info(
                f"[{requester_ip}] {method} /{domain}{path} {status_code} -> {duration:.3f} sec "
                f"Browser: {user_agent} Ref: {referer}",
            )

        return response
