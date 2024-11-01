import base64
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def encrypt_json(data: dict) -> dict:
    key = load_key()
    initialization_vector = os.urandom(int(os.getenv('AES_ENCRYPTION_IV')))

    json_data = json.dumps(data).encode('utf-8')

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(json_data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(initialization_vector), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = initialization_vector + encryptor.update(padded_data) + encryptor.finalize()
    base64_encoded = base64.b64encode(encrypted_data).decode('utf-8')

    return {'data': base64_encoded}


def load_key() -> bytes:
    with open('AES_ENCRYPTION_KEY.bin', 'rb') as key_file:
        key = key_file.read()
    return key
