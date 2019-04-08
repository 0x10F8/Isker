import requests

DATASOURCE = 'tranquility'
VERSION = 'v1'
BASE_URL = 'https://esi.evetech.net'


def get_url():
    return BASE_URL + '/' + VERSION


def build_url(path):
    return get_url() + '/' + path


def do_get(path, params):
    url = build_url(path)
    params['datasource'] = DATASOURCE
    response = requests.get(url=url, params=params)
    return response.json()
