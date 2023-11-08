from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from .utils import fail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(response, APIException):
        return response
    error = APIException(fail(response))
    error.status_code = 500
    return error
