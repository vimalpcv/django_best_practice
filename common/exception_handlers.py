# myproject/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from common.error import UNAUTHORIZED


def custom_exception_handler(exc, context):
    # Call the default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        error = UNAUTHORIZED['error']
        error['detail'] = response.data['detail']
        response.data = error

    return response
