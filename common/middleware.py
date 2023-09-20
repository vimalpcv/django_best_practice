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
                data = json.loads(request.body.decode("utf-8")).get("data", None)
                if data:
                    if self.ENCRYPT and type(data) == str:
                        encrypted_data = CommonUtils.b64_decode(data.encode("utf-8"))
                        decrypted_data, error = Cipher.decrypt(encrypted_data)
                        if not error:
                            decrypted_data = decrypted_data.decode('utf-8').replace("'", '"')
                            decrypted_data = ('{"data": ' + decrypted_data + '}')
                            request._body = decrypted_data.encode("utf-8")
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

        if self.ENCRYPT and response.status_code == 200:
            data = json.loads(response.content.decode("utf-8"))
            data["data"] = Cipher.encrypt(str(data["data"]).encode("utf-8"))
            response.content = json.dumps(data).encode("utf-8")

        return response
