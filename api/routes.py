from api import api


def get_route(from_id, to_id):
    return api.do_get(1, 'route/' + str(from_id) + '/' + str(to_id), {})
