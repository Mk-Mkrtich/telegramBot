import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import json


def decrypt_json(data: dict) -> dict:
    base64_encoded = data['data']
    encrypted_data = base64.b64decode(base64_encoded)

    encryption_iv = int(os.getenv('AES_ENCRYPTION_IV'))
    key = load_key()

    initialization_vector = encrypted_data[:encryption_iv]
    ciphertext = encrypted_data[encryption_iv:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(initialization_vector), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(padded_text) + unpadder.finalize()

    return json.loads(decrypted_data.decode('utf-8'))


def load_key() -> bytes:
    with open('AES_ENCRYPTION_KEY.bin', 'rb') as key_file:
        key = key_file.read()
    return key

