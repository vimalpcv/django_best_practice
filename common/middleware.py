import json
from django.http import JsonResponse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from django.conf import settings

from .error import DECRYPTION_ERROR, ENCRYPTION_NOT_ENABLED, ENCRYPTION_ENABLED
from .utils import CommonUtils


class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = settings.AES_SECRET_KEY.encode('utf-8')
        self.ENCRYPT = settings.ENCRYPT

    def encrypt(self, data: bytes):
        nonce = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce)
        cipher_text, tag = cipher.encrypt_and_digest(data)
        encrypted_data = nonce + cipher_text + tag
        b64_encrypted_data = CommonUtils.b64_encode(encrypted_data)
        return b64_encrypted_data

    def decrypt(self, encrypted_data: bytes):
        try:
            nonce = encrypted_data[:16]
            tag = encrypted_data[-16:]
            cipher_text = encrypted_data[16:-16]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce)
            decrypted_data = cipher.decrypt_and_verify(cipher_text, tag)
            decrypted_data = decrypted_data.decode('utf-8')
            return decrypted_data, None
        except Exception as e:
            return None, str(e)

    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            data = json.loads(request.body.decode('utf-8')).get('data', None)
            if data:
                if self.ENCRYPT and type(data) == str:
                    encrypted_data = CommonUtils.b64_decode(data.encode('utf-8'))
                    decrypted_data, error = self.decrypt(encrypted_data)
                    if not error:
                        decrypted_data = eval(json.dumps('{"data": ' + decrypted_data + '}'))
                        request._body = decrypted_data.encode('utf-8')
                    else:
                        data = {
                            'code': DECRYPTION_ERROR['code'],
                            'message': DECRYPTION_ERROR['message'] + ': ' + error
                        }
                        return JsonResponse(data, status=DECRYPTION_ERROR['status'])
                elif self.ENCRYPT and type(data) == dict:
                    data = {
                        'code': ENCRYPTION_ENABLED['code'],
                        'message': ENCRYPTION_ENABLED['message']
                    }
                    return JsonResponse(data, status=ENCRYPTION_ENABLED['status'])
                elif not self.ENCRYPT and type(data) == str:
                    if type(data) == str:
                        data = {
                            'code': ENCRYPTION_NOT_ENABLED['code'],
                            'message': ENCRYPTION_NOT_ENABLED['message']
                        }
                        return JsonResponse(data, status=ENCRYPTION_NOT_ENABLED['status'])

        # -----------
        response = self.get_response(request)
        # -----------

        if self.ENCRYPT:
            response.content = self.encrypt(response.content)

        return response
