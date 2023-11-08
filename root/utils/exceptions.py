from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .utils import fail


def exception_handler(exc, context):
    if isinstance(exc, APIException):
        return Response(fail(exc.detail), status=exc.status_code if exc.status_code else 500)
    return Response(fail(str(exc)), status=500)
