from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from django.conf import settings
from typing import Union, Tuple


class CipherManager:
    def __init__(self):
        self.key = settings.ENCRYPTION_KEY.encode('utf-8')
        self.ENCRYPT = settings.ENCRYPT

    def encrypt(self, data: bytes) -> bytes | None:
        try:
            nonce = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_GCM, nonce)
            cipher_text, tag = cipher.encrypt_and_digest(data)
            encrypted_data = nonce + cipher_text + tag
            return encrypted_data
        except:
            return None

    def decrypt(self, encrypted_data: bytes) -> Tuple[bytes | None, str | None]:
        try:
            nonce = encrypted_data[:16]
            tag = encrypted_data[-16:]
            cipher_text = encrypted_data[16:-16]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce)
            decrypted_data = cipher.decrypt_and_verify(cipher_text, tag)
            return decrypted_data, None
        except Exception as e:
            return None, str(e)
