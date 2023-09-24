import json
from django.http import JsonResponse
from django.conf import settings
from common.error import DECRYPTION_ERROR, ENCRYPTION_NOT_ENABLED, ENCRYPTION_ENABLED, INTERNAL_SERVER_ERROR
from common.utils import CommonUtils
from common.mangers import Cipher


class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ENCRYPT = settings.ENCRYPT

    def __call__(self, request):
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
                if data:
                    if self.ENCRYPT and type(data) == str:
                        encrypted_data = CommonUtils.b64_decode(data.encode("utf-8"))
                        decrypted_data, error = Cipher.decrypt(encrypted_data)
                        if not error:
                            request._body = decrypted_data
                        else:
                            response_data = DECRYPTION_ERROR["error"]
                            response_data["detail"] = str(error)
                            return JsonResponse(response_data, status=DECRYPTION_ERROR["status_code"])
                    elif self.ENCRYPT and type(data) == dict:
                        return JsonResponse(ENCRYPTION_ENABLED["error"], status=ENCRYPTION_ENABLED["status_code"])
                    elif not self.ENCRYPT and type(data) == str:
                        if type(data) == str:
                            return JsonResponse(ENCRYPTION_NOT_ENABLED["error"], status=ENCRYPTION_NOT_ENABLED["status_code"])
                    else:
                        request._body = request.body
                else:
                    request._body = "{}".encode("utf-8") if request.body == b'' else request.body
        except Exception as e:
            response_data = INTERNAL_SERVER_ERROR["error"]
            response_data["detail"] = str(e)
            return JsonResponse(response_data, status=INTERNAL_SERVER_ERROR["status_code"])

        # -----------
        response = self.get_response(request)
        # -----------
        if hasattr(response, 'data') and 200 <= response.status_code < 300:
            response.data = CommonUtils.b64_encode(Cipher.encrypt(str(response.data).encode('utf-8')))
            response._is_rendered = False
            response.render()
        return response
