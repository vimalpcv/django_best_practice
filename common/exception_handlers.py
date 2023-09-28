from rest_framework.views import exception_handler
from common.error import UNAUTHORIZED


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error = UNAUTHORIZED['error']
        error['detail'] = response.data.get('detail')
        if not error['detail']:
            error['detail'] = response.data['non_field_errors'][0]

        response.data = error

    return response
