import seed
from data import filestore
from api import routes

if not filestore.do_files_exist():
    seed.seed_data_store()

print('Loading data from file...')

# Get all the region ids
regions_ids = filestore.load_region_ids()

# Get region info
region_infos = filestore.load_region_info()

# Get market data for each region
market_datas = filestore.load_market_data()

# Create a list of all the unique market location ids
location_ids = filestore.load_location_ids()

# Get the location information
locations = filestore.load_location_info()

# Get all the buy and sell orders
buy_orders = filestore.load_buy_orders()
sell_orders = filestore.load_sell_orders()

# Get system info
system_ids = filestore.load_system_ids()
system_infos = filestore.load_system_info()


def is_high_sec_order(order, system_infos):
    """
    Check if order is in high sec
    :param order: the order
    :param system_infos: the dictionary of system info
    :return: true or false
    """
    system_id = order['system_id']
    system_info = system_infos[str(system_id)]
    return system_info['security_status'] >= 0.5


def is_valid_location(location):
    is_valid = False
    if location is not None:
        if 'error' not in location.keys():
            is_valid = True
    return is_valid


def filter_orders_to_system(orders, location_infos, system_name):
    filtered = []
    for order in orders:
        location_info = location_infos[str(order['location_id'])]
        if is_valid_location(location_info) and system_name in location_info['name']:
            filtered.append(order)
    return filtered


# Filter out the low/null orders
print('Filtering out low and null orders...')
buy_orders = [order for order in buy_orders if is_high_sec_order(order, system_infos)]
sell_orders = [order for order in sell_orders if is_high_sec_order(order, system_infos)]

# Item type ids
type_ids = filestore.load_type_ids()

# Get the item information
types = filestore.load_type_info()


def get_order_string(order):
    """
    Get a string representation of an order
    :param order: the order
    :return: string of the order system, item, price, units
    """
    item = types[str(order['type_id'])]['name']
    system = system_infos[str(order['system_id'])]['name']
    price = order['price']
    units = order['volume_remain']
    return '(' + str(system) + '    ' + str(item) + '   ' + '{:,}'.format(price) + '   ' + '{:,}'.format(units) + ')'


def get_min_units(sell_order, buy_order):
    """
    Get the minimum units between orders
    :param sell_order: sell order
    :param buy_order: buy order
    :return: minimum units between orders
    """
    sell_units = sell_order['volume_remain']
    buy_units = buy_order['volume_remain']
    return min(sell_units, buy_units)


def get_total_profit(sell_order, buy_order):
    """
    Calculate the total profit for a trade
    :param sell_order: The sell order you will buy from
    :param buy_order:  The buy order you will sell to
    :return: the total profit considering units available to trade
    """
    sell_price = sell_order['price']
    buy_price = buy_order['price']
    min_units = get_min_units(sell_order, buy_order)
    total_sell_price = sell_price * min_units
    total_buy_price = buy_price * min_units
    return total_buy_price - total_sell_price


def print_trade(sell_order, buy_order):
    """
    Print out a trade
    :param sell_order: The sell order you will buy from
    :param buy_order:  The buy order you will sell to
    :return: nothing
    """
    total_cost = get_min_units(sell_order, buy_order) * sell_order['price']
    total_profit = get_total_profit(sell_order, buy_order)
    route = routes.get_route(sell_order['system_id'], buy_order['system_id'])
    print('--')
    print('Buy here:        ' + get_order_string(sell_order))
    print('Sell here:       ' + get_order_string(buy_order))
    print('Route jumps      ' + str(len(route)))
    print('Total Cost:      ' + '{:,}'.format(total_cost))
    print('Units to trade:  ' + '{:,}'.format(get_min_units(sell_order, buy_order)))
    print(
        'Total Profit:    ' + '{:,}'.format(round(total_profit, 2)) + ' (' + '{:,}'.format(
            round((total_profit / total_cost * 100), 2)) + '%)')
    print('--')


def find_sell_to_buy(buy_orders_by_type, sell_orders_by_type, threshold_buy_value, min_profit_percent):
    """
    Try to find profitable orders
    :param buy_orders_by_type: dictionary of buy orders to type id
    :param sell_orders_by_type: dictionary of sell orders to type id
    :param threshold_buy_value: threshold buy value (don't consider trades where the units*cost is less than this)
    :param min_profit_percent: minimum profit % just on unit price
    :return: list of tuples of possibly profitable trades
    """
    profitable = []
    for type_id in type_ids:
        if type_id in sell_orders_by_type.keys() and type_id in buy_orders_by_type.keys():
            # Gather the orders for this type
            type_sell_orders = sell_orders_by_type[type_id]
            type_buy_orders = buy_orders_by_type[type_id]

            # Setup something to hold the lowest sell order and highest buy order
            lowest_sell_order = None
            highest_buy_order = None

            # Calculate the lowest sell order
            for sell_order in type_sell_orders:
                sell_price = sell_order['price']
                sell_units = sell_order['volume_remain']
                sell_total = sell_price * sell_units
                if lowest_sell_order is not None:
                    if sell_price < lowest_sell_order['price'] and sell_total >= threshold_buy_value:
                        lowest_sell_order = sell_order
                else:
                    lowest_sell_order = sell_order

            # Calculate the highest buy order
            for buy_order in type_buy_orders:
                buy_price = buy_order['price']
                buy_units = buy_order['volume_remain']
                buy_total = buy_price * buy_units
                if highest_buy_order is not None:
                    if buy_price > highest_buy_order['price'] and buy_total >= threshold_buy_value:
                        highest_buy_order = buy_order
                else:
                    highest_buy_order = buy_order

            if lowest_sell_order is not None and highest_buy_order is not None:
                total_profit_per_item = highest_buy_order['price'] - lowest_sell_order['price']
                profit_percent = total_profit_per_item / lowest_sell_order['price'] * 100
                if profit_percent >= min_profit_percent:
                    profitable.append((lowest_sell_order, highest_buy_order))
    return profitable


def find_sell_to_sell(sell_orders_by_type_dest, sell_orders_by_type_orig, threshold_buy_value, min_profit_percent):
    """
    Try to find profitable orders
    :param sell_orders_by_type_dest:
    :param sell_orders_by_type_orig:
    :param threshold_buy_value: threshold buy value (don't consider trades where the units*cost is less than this)
    :param min_profit_percent: minimum profit % just on unit price
    :return: list of tuples of possibly profitable trades
    """
    profitable = []
    for type_id in type_ids:
        if type_id in sell_orders_by_type_dest.keys() and type_id in sell_orders_by_type_orig.keys():
            # Gather the orders for this type
            type_sell_orders_orig = sell_orders_by_type_orig[type_id]
            type_buy_orders_dest = sell_orders_by_type_dest[type_id]

            lowest_sell_order_orig = None
            lowest_sell_order_dest = None

            for sell_order in type_sell_orders_orig:
                sell_price = sell_order['price']
                sell_units = sell_order['volume_remain']
                sell_total = sell_price * sell_units
                if lowest_sell_order_orig is not None:
                    if sell_price < lowest_sell_order_orig['price'] and sell_total >= threshold_buy_value:
                        lowest_sell_order_orig = sell_order
                else:
                    lowest_sell_order_orig = sell_order

            for buy_order in type_buy_orders_dest:
                buy_price = buy_order['price']
                buy_units = buy_order['volume_remain']
                buy_total = buy_price * buy_units
                if lowest_sell_order_dest is not None:
                    if buy_price < lowest_sell_order_dest['price'] and buy_total >= threshold_buy_value:
                        lowest_sell_order_dest = buy_order
                else:
                    lowest_sell_order_dest = buy_order

            if lowest_sell_order_orig is not None and lowest_sell_order_dest is not None:
                total_profit_per_item = lowest_sell_order_dest['price'] - lowest_sell_order_orig['price']
                profit_percent = total_profit_per_item / lowest_sell_order_orig['price'] * 100
                if profit_percent >= min_profit_percent:
                    profitable.append((lowest_sell_order_dest, lowest_sell_order_orig))
    return profitable


##buy_orders = filter_orders_to_system(buy_orders, locations, 'Jita')
##sell_orders = filter_orders_to_system(sell_orders, locations, 'Jita')

buy_orders_by_type = {}
# Map the orders to the type of item
for order in buy_orders:
    type_id = order['type_id']
    if type_id not in buy_orders_by_type.keys():
        buy_orders_by_type[type_id] = []
    buy_orders_by_type[type_id].append(order)

sell_orders_by_type = {}
# Map the orders to the type of item
for order in sell_orders:
    type_id = order['type_id']
    if type_id not in sell_orders_by_type.keys():
        sell_orders_by_type[type_id] = []
    sell_orders_by_type[type_id].append(order)

# Find profitable trades
print('Finding profitable trades...')
profitable_trades = find_sell_to_buy(buy_orders_by_type, sell_orders_by_type, 100, 3)

# Print out actually profitable trades within a threshold
profit_threshold = 1000000
for sell, buy in profitable_trades:
    if get_total_profit(sell, buy) >= profit_threshold:
        print_trade(sell, buy)
