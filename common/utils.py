import base64, logging, json
from rest_framework.response import Response


class CommonUtils:

    @staticmethod
    def b64_encode(data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def b64_decode(data: bytes) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def dispatch_success(request, response='SUCCESS'):
        try:
            response = {'status': 'SUCCESS', 'data': response}

            # logging the success response
            extras = {
                'status': 'SUCCESS',
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': str(response),
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info('Request Successful', extra=extras)

            return Response(response, status=200)
        except Exception as e:
            print('Exception in dispatch_success', str(e))

    @staticmethod
    def dispatch_failure(request, error, error_message=None):
        try:
            response_data = {
                'status': 'FAILED',
                'code': error['code'],
                'message': error['message'] + ": " + str(error_message) if error_message else error['message']
            }

            response = Response(response_data, status=error['status'])

            # logging the failure response
            extras = {
                'status': 'FAILED',
                'method': request.method,
                'url': request.path,
                'request_data': request.data,
                'response_data': str(response),
                'user': request.user,
            }
            logger = logging.getLogger('request')
            logger.info(response_data['message'], extra=extras)

            return Response(response_data, status=error['status'])
        except Exception as e:
            print('Exception in dispatch_failure', str(e))

