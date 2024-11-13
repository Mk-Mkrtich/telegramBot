from admin.encoding import encrypt_json
from admin.decode import decrypt_json
import requests
import os


def admin_call(data: dict or None, url, method="GET"):
    response = None
    try:
        full_url = os.getenv('ADMIN_PROTOKOL') + os.getenv('ADMIN_HOST') + os.getenv('ADMIN_PORT') + '/' + url
        headers = {
            'TBTOKEN': os.getenv('ADMIN_TOKEN'),
            'Content-Type': 'application/json',
        }
        if data:
            data = encrypt_json(data)
        if method == 'GET':
            response = requests.get(full_url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(full_url, headers=headers, json=data)
        response.raise_for_status()
        response_data = decrypt_json(response.json())
        return {"code": response.status_code, "data": response_data}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"code": response.status_code, "data": http_err}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"code": 500, "data": err}
