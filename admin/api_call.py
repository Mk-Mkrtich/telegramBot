import requests
import os


def admin_call(data, url, method):
    response = None
    try:
        full_url = os.getenv('ADMIN_PROTOKOL') + os.getenv('ADMIN_HOST') + os.getenv('ADMIN_PORT') + '/' + url
        headers = {
            'TBTOKEN': os.getenv('ADMIN_TOKEN'),
            'Content-Type': 'application/json',
        }
        if method == 'GET':
            response = requests.get(full_url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(full_url, headers=headers, json=data)
        response.raise_for_status()
        return {"code": response.status_code, "data": response.json()}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"code": response.status_code, "data": http_err}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"code": response.status_code, "data": err}
