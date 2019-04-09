from api import api


def get_all_region_orders(id):
    return api.do_get(1, 'markets/' + str(id) + '/orders/', {})

