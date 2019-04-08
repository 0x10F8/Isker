import requests

DATASOURCE = 'tranquility'
BASE_URL = 'https://esi.evetech.net'
RETRIES = 10


def build_url(version, path):
    return BASE_URL + '/' + 'v' + str(version) + '/' + path


def do_get(version, path, params):
    return do_get_retry(version, path, params, RETRIES)


def do_get_retry(version, path, params, retries_remaining):
    if retries_remaining > 0:
        url = build_url(version, path)
        params['datasource'] = DATASOURCE
        try:
            response = requests.get(url=url, params=params).json()
        except:
            response = do_get_retry(version, path, params, (retries_remaining - 1))
        return response
