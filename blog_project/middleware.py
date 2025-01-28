import logging
from datetime import datetime
import traceback

logger = logging.getLogger("my_custom_logger")


class RequestLoggingMiddleware:
    """
    Middleware to log incoming HTTP requests and their responses.
    Logs errors if they occur during request handling.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)
        try:
            response = self.get_response(request)
            self.log_response(response)
        except Exception as e:
            self.log_error(request, e)
            raise e
        return response

    def log_request(self, request):
        """
        Logs details about the incoming request.
        """
        logger.info(
            f"Incoming request: {request.method} {request.path} | "
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'} | "
            f"IP: {request.META.get('REMOTE_ADDR', 'Unknown IP')} | "
            f"Headers: {dict(request.headers)} | "
            f"Timestamp: {datetime.now()}"
        )

    def log_response(self, response):
        """
        Logs the response status code.
        """
        logger.info(
            f"Response status code: {response.status_code} | "
            f"Timestamp: {datetime.now()}"
        )

    def log_error(self, request, exception):
        """
        Logs errors if any exception is raised during request processing.
        """
        logger.error(
            f"Error processing request: {request.method} {request.path} | "
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'} | "
            f"IP: {request.META.get('REMOTE_ADDR', 'Unknown IP')} | "
            f"Error: {str(exception)} | "
            f"Traceback: {traceback.format_exc()} | "
            f"Timestamp: {datetime.now()}"
        )
