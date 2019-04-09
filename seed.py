from api import universe, market
from data import filestore


def get_all_buy_orders(market_datas):
    """
    Get all buy orders from the returned market data
    :param market_datas: the market data dictionary
    :return: list of buy orders
    """
    buy_orders = []
    for _, market_data in market_datas.items():
        for order in market_data:
            if order['is_buy_order']:
                buy_orders.append(order)
    return buy_orders


def get_all_sell_orders(market_datas):
    """
    Get all sell orders from the returned market data
    :param market_datas: the market data dictionary
    :return: list of sell orders
    """
    sell_orders = []
    for _, market_data in market_datas.items():
        for order in market_data:
            if not order['is_buy_order']:
                sell_orders.append(order)
    return sell_orders


def get_all_unique_type_ids(market_datas):
    """
    Get all unique type ids from market data
    :param market_datas: the market data dictionary
    :return: list of type ids
    """
    type_ids = []
    for _, market_data in market_datas.items():
        for order in market_data:
            type_id = order['type_id']
            if type_id not in type_ids:
                type_ids.append(type_id)
    return type_ids


def get_all_unique_location_ids(market_datas):
    """
    Get all unique location ids from the market data
    :param market_datas: the market data dictionary
    :return: list of locations ids
    """
    location_ids = []
    for _, market_data in market_datas.items():
        for order in market_data:
            location_id = order['location_id']
            if location_id not in location_ids:
                location_ids.append(location_id)
    return location_ids


def seed_data_store():
    """
    Seed all of the file stores
    :return: nothing
    """
    print('Loading region ids...')

    # Get all the region ids
    regions_ids = universe.get_region_ids()

    # Store region ids
    filestore.store_region_ids(regions_ids)

    print('Loading region info...')

    # Get region info
    region_infos = {region_id: universe.get_region_info(region_id) for region_id in regions_ids}

    # Store the region info
    filestore.store_region_info(region_infos)

    print('Loading market data for regions...')

    # Get market data for each region
    market_datas = {region_id: market.get_all_region_orders(region_id) for region_id in regions_ids}

    # Store the market data
    filestore.store_market_data(market_datas)

    print('Loading location ids from orders...')
    # Create a list of all the unique market location ids
    location_ids = get_all_unique_location_ids(market_datas)

    # Store the location ids
    filestore.store_location_ids(location_ids)

    print('Loading location info...')
    # Get the location information
    locations = {location_id: (universe.get_station_info(location_id)
                               if location_id <= universe.STATION_ID_LIMIT
                               else universe.get_structure_info(location_id))
                 for location_id in location_ids}

    # Store the location info
    filestore.store_location_info(locations)

    print('Parsing buy and sell orders...')
    # Get all the buy and sell orders
    buy_orders = get_all_buy_orders(market_datas)
    sell_orders = get_all_sell_orders(market_datas)

    # Store the buy and sell orders
    filestore.store_buy_orders(buy_orders)
    filestore.store_sell_orders(sell_orders)

    print('Loading type ids from orders...')
    # Item type ids
    type_ids = get_all_unique_type_ids(market_datas)

    # Store type ids
    filestore.store_type_ids(type_ids)

    print('Loading type info...')
    # Get the item information
    types = {type_id: universe.get_type_info(type_id) for type_id in type_ids}

    # Store type info
    filestore.store_type_info(types)
