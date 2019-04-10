from api import api

PAGES = 300


def get_all_region_orders(id):
    orders = []
    for page in range(1, PAGES):
        page_orders = api.do_get(1, 'markets/' + str(id) + '/orders/', {'page': page})
        if len(page_orders) > 1:
            orders.extend(page_orders)
        else:
            continue
    return orders
