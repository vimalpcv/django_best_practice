import base64, logging, json
from rest_framework.response import Response
from django.conf import settings
from common.mangers import Cipher
from common.logger import info_log, error_log


class CommonUtils:

    @staticmethod
    def b64_encode(data: bytes) -> bytes:
        return base64.b64encode(data)

    @staticmethod
    def b64_decode(data: bytes) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def dispatch_success(request, response_data=None, status_code=200):
        try:
            # logging the success response
            extras = {
                'status': 'SUCCESS',
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': str(response_data),
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info('Request Successful', extra=extras)

            if settings.ENCRYPT:
                response_data = CommonUtils.b64_encode(Cipher.encrypt(str(response_data).encode('utf-8')))

            return Response(response_data, status=status_code)
        except Exception:
            error_log(request)

    @staticmethod
    def dispatch_failure(request, error, error_message=None):
        try:

            response_data = error['error']
            if error_message:
                response_data['detail'] = error_message



            # logging the failure response
            extras = {
                'status': 'FAILED',
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': str(response_data),
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info(response_data['message'], extra=extras)

            if settings.ENCRYPT:
                response_data = CommonUtils.b64_encode(Cipher.encrypt(str(response_data).encode('utf-8')))

            return Response(response_data, status=error['status_code'])
        except Exception as e:
            print('Exception in dispatch_failure', str(e))

