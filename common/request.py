# coding: utf-8
# @Author: bgtech
import requests

def send_request(method, url, data=None, headers=None):
    if method.lower() == 'get':
        response = requests.get(url, params=data, headers=headers)
    elif method.lower() == 'post':
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError("Unsupported HTTP method")
    return response.json()