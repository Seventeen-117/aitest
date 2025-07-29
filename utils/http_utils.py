import requests

def http_get(url, params=None, headers=None, token=None, **kwargs):
    headers = headers or {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    response = requests.get(url, params=params, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()

def http_post(url, data=None, json_data=None, headers=None, token=None, **kwargs):
    headers = headers or {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    response = requests.post(url, data=data, json=json_data, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()