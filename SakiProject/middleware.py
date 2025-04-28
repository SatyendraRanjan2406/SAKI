#  This middleware will catch any unhandled exception and return a JSON error.
#
#  It will log the error into Django’s logging system (exc_info=True gives full traceback).
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Unhandled Exception: {str(exception)}", exc_info=True)

        response_data = {
            "success": False,
            "error": str(exception)  # You can hide detailed errors in production
        }
        return JsonResponse(response_data, status=500)
