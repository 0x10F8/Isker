from api import api

PAGES = 100


def get_all_region_orders(id):
    orders = []
    for page in range(1, PAGES):
        orders.extend(api.do_get(1, 'markets/' + str(id) + '/orders/', {'page': page}))
    return orders
