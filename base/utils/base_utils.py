import base64, logging, copy
from rest_framework.response import Response
from base.logger import error_log
from base.constants import SUCCESS, FAILURE
from base.error import INTERNAL_SERVER_ERROR


class BaseUtils:

    @staticmethod
    def b64_encode(data: bytes) -> bytes:
        return base64.b64encode(data)

    @staticmethod
    def b64_decode(data: bytes) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def dispatch_success(request, data: dict | None = None, status_code=200) -> Response:
        try:
            # logging the success response
            extras = {
                'status': SUCCESS,
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': data,
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info('Request Completed', extra=extras)
            return Response(data, status=status_code)
        except Exception as e:
            error_log(request)
            error = copy.deepcopy(INTERNAL_SERVER_ERROR['error'])
            error['detail'] = str(e)
            return Response(error, status=500)

    @staticmethod
    def dispatch_failure(request, error: dict, data: str | dict | None = None) -> Response:
        try:
            response_data = error['error']
            if data:
                response_data['detail'] = data

            # logging the failure response
            extras = {
                'status': FAILURE,
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': str(response_data),
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info(response_data['message'], extra=extras)

            return Response(response_data, status=error['status_code'])
        except Exception as e:
            error_log(request)
            error = copy.deepcopy(INTERNAL_SERVER_ERROR['error'])
            error['detail'] = str(e)
            return Response(error, status=500)
